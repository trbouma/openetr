"""Exercise the deployment script without Git/network/container mutations."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).parents[1]
STUB = r'''
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
name = Path(sys.argv[0]).name
with open(os.environ['CALLS'], 'a') as f: f.write(json.dumps([name,*args])+'\n')
if name == 'git':
    if args[:1] == ['diff'] and os.environ.get('FAIL') == 'dirty': sys.exit(1)
    if args[:1] == ['rev-parse']: print('testrevision')
    sys.exit()
if args == ['compose','up','--help']:
    print('unsupported' if os.environ.get('FAIL') == 'old' else '--wait --wait-timeout'); sys.exit()
if args[:2] == ['compose','config'] and os.environ.get('FAIL') == 'config': sys.exit(1)
if args[:2] == ['compose','build'] and os.environ.get('FAIL') == 'build': sys.exit(1)
if args[:2] == ['compose','up'] and os.environ.get('FAIL') == 'wait': sys.exit(1)
if args[:4] == ['compose','ps','--all','--quiet']: print('abc123')
if args[:1] == ['inspect']: print('health diagnostic')
if args[:2] == ['compose','logs']: print('recent logs')
'''


def run(tmp_path, args=(), failure=''):
    shutil.copy2(ROOT/'refresh-containers.sh', tmp_path/'refresh-containers.sh')
    for name in ('git', 'docker'):
        p=tmp_path/name
        p.write_text('#!'+sys.executable+'\n'+STUB)
        p.chmod(0o755)
    calls=tmp_path/'calls'
    result=subprocess.run(['sh',str(tmp_path/'refresh-containers.sh'),*args],
        env={**os.environ,'PATH':str(tmp_path)+os.pathsep+os.environ['PATH'],
             'CALLS':str(calls),'FAIL':failure},capture_output=True,text=True,timeout=10)
    commands=[json.loads(line) for line in calls.read_text().splitlines()] if calls.exists() else []
    assert not any(c[:3] in [['docker','compose','down'],['docker','compose','stop']] for c in commands)
    return result,commands


def up(commands):
    return [c for c in commands if c[:3]==['docker','compose','up'] and '--help' not in c]


def test_waits_for_entire_stack(tmp_path):
    result,commands=run(tmp_path,('--timeout','180'))
    assert result.returncode==0,result.stderr
    assert up(commands)==[['docker','compose','up','--force-recreate','--detach','--wait','--wait-timeout','180']]
    assert ['git','pull','--ff-only'] in commands
    assert not any('exec' in c for c in commands)  # no web-only readiness shortcut


@pytest.mark.parametrize('failure',['dirty','old','config','build'])
def test_preflight_or_build_failure_never_recreates(tmp_path,failure):
    result,commands=run(tmp_path,failure=failure)
    assert result.returncode!=0 and not up(commands)


def test_worker_or_other_service_failure_reports_diagnostics(tmp_path):
    result,commands=run(tmp_path,failure='wait')
    assert result.returncode!=0
    assert 'health diagnostic' in result.stderr and 'recent logs' in result.stderr
    assert 'passed their readiness' not in result.stdout
    assert any(c[:3]==['docker','compose','logs'] for c in commands)


@pytest.mark.parametrize('args',[('--timeout','0'),('--timeout','3601'),('--timeout','abc'),('--unknown',)])
def test_rejects_bad_arguments_before_commands(tmp_path,args):
    result,commands=run(tmp_path,args)
    assert result.returncode==2 and not commands
