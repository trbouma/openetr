import click
from etrix.commands.core import hello, init_config, set_config, version
from etrix.commands.publish import publish_object
from etrix.commands.query import query_object, query_profile


@click.group()
def main() -> None:
    """ETRix command line utility."""


main.add_command(version)
main.add_command(init_config)
main.add_command(set_config)
main.add_command(hello)
main.add_command(publish_object)
main.add_command(query_object)
main.add_command(query_profile)
