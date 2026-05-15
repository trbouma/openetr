from __future__ import annotations

import hashlib
import json
from base64 import urlsafe_b64encode
from typing import Literal

from cryptography.fernet import Fernet, InvalidToken
from starlette.datastructures import MutableHeaders, Secret
from starlette.middleware.sessions import Session
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class EncryptedSessionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        secret_key: str | Secret,
        session_cookie: str = "session",
        max_age: int | None = 14 * 24 * 60 * 60,
        path: str = "/",
        same_site: Literal["lax", "strict", "none"] = "lax",
        https_only: bool = False,
        domain: str | None = None,
    ) -> None:
        self.app = app
        self.fernet = Fernet(self._derive_fernet_key(str(secret_key)))
        self.session_cookie = session_cookie
        self.max_age = max_age
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site
        if https_only:
            self.security_flags += "; secure"
        if domain is not None:
            self.security_flags += f"; domain={domain}"

    @staticmethod
    def _derive_fernet_key(secret_key: str) -> bytes:
        digest = hashlib.sha256(secret_key.encode("utf-8")).digest()
        return urlsafe_b64encode(digest)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_session_was_empty = True

        if self.session_cookie in connection.cookies:
            token = connection.cookies[self.session_cookie].encode("utf-8")
            try:
                data = self.fernet.decrypt(token, ttl=self.max_age) if self.max_age else self.fernet.decrypt(token)
                scope["session"] = Session(json.loads(data.decode("utf-8")))
                initial_session_was_empty = False
            except (InvalidToken, json.JSONDecodeError):
                scope["session"] = Session()
        else:
            scope["session"] = Session()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                session: Session = scope["session"]
                headers = MutableHeaders(scope=message)
                if session.accessed:
                    headers.add_vary_header("Cookie")
                if session.modified and session:
                    payload = json.dumps(dict(session), separators=(",", ":")).encode("utf-8")
                    token = self.fernet.encrypt(payload)
                    header_value = "{session_cookie}={data}; path={path}; {max_age}{security_flags}".format(
                        session_cookie=self.session_cookie,
                        data=token.decode("utf-8"),
                        path=self.path,
                        max_age=f"Max-Age={self.max_age}; " if self.max_age else "",
                        security_flags=self.security_flags,
                    )
                    headers.append("Set-Cookie", header_value)
                elif session.modified and not initial_session_was_empty:
                    header_value = "{session_cookie}={data}; path={path}; {expires}{security_flags}".format(
                        session_cookie=self.session_cookie,
                        data="null",
                        path=self.path,
                        expires="expires=Thu, 01 Jan 1970 00:00:00 GMT; ",
                        security_flags=self.security_flags,
                    )
                    headers.append("Set-Cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)
