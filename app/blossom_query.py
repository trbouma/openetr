"""Restricted, digest-verified retrieval from a user-selected Blossom server."""

import hashlib
import http.client
import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit


def normalize_server(value: str) -> str:
    value = value.strip().rstrip("/")
    try:
        parts = urlsplit(value)
        valid = (parts.scheme == "https" and parts.hostname and not parts.username
                 and not parts.password and parts.port in (None, 443)
                 and not parts.query and not parts.fragment)
    except ValueError:
        valid = False
    if not valid or any(ord(char) <= 32 for char in value):
        raise ValueError("Use a public HTTPS Blossom server URL on port 443, without credentials, query, or fragment.")
    return value


def fetch_verified(digest: str, server: str, *, timeout: float, max_bytes: int):
    parts = urlsplit(normalize_server(server))
    addresses = socket.getaddrinfo(parts.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("The Blossom server must resolve only to public IP addresses.")
    connection = http.client.HTTPSConnection(parts.hostname, timeout=timeout)
    # Pin the checked destination while retaining hostname-based TLS verification.
    address = addresses[0][4][0]
    connection._create_connection = lambda *args, **kwargs: socket.create_connection((address, 443), timeout=timeout)
    try:
        path = urlunsplit(("", "", f"{parts.path.rstrip('/')}/{digest}", "", ""))
        connection.request("GET", path)
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError(f"Blossom retrieval returned HTTP {response.status}. Redirects are not followed.")
        content = response.read(max_bytes + 1)
        if len(content) > max_bytes:
            raise ValueError("The Blossom artifact exceeds the download limit.")
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError("The retrieved artifact does not match the requested SHA-256 digest.")
        return content, response.getheader("Content-Type")
    finally:
        connection.close()
