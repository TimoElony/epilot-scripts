"""
Epilot Scripts Library

Core utilities for interacting with Epilot APIs.
"""

from .api_client import EpilotClient
from .auth import load_env, get_auth_headers

__all__ = ["EpilotClient", "load_env", "get_auth_headers"]
