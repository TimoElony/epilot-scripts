"""
Epilot API Client

A simple, reusable HTTP client for making requests to Epilot APIs.
"""

import httpx
import asyncio
from typing import Any, Dict, Optional, List
from .auth import get_auth_headers

class EpilotClient:
    """
    Simple HTTP client for Epilot API interactions.
    
    Usage:
        client = EpilotClient()
        result = await client.get("https://entity.sls.epilot.io/v1/entities")
    """
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = get_auth_headers()
    
    async def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a GET request."""
        headers = {**self.headers, **(custom_headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a POST request."""
        headers = {**self.headers, **(custom_headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        headers = {**self.headers, **(custom_headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.put(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def delete(
        self,
        url: str,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a DELETE request."""
        headers = {**self.headers, **(custom_headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(url, headers=headers)
            response.raise_for_status()
            if response.content:
                return response.json()
            return {"status": "success"}
    
    async def patch(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        headers = {**self.headers, **(custom_headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.patch(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    # Synchronous wrappers for convenience
    def get_sync(self, url: str, **kwargs) -> Dict[str, Any]:
        """Synchronous GET request."""
        return asyncio.run(self.get(url, **kwargs))
    
    def post_sync(self, url: str, **kwargs) -> Dict[str, Any]:
        """Synchronous POST request."""
        return asyncio.run(self.post(url, **kwargs))
    
    def put_sync(self, url: str, **kwargs) -> Dict[str, Any]:
        """Synchronous PUT request."""
        return asyncio.run(self.put(url, **kwargs))
    
    def delete_sync(self, url: str, **kwargs) -> Dict[str, Any]:
        """Synchronous DELETE request."""
        return asyncio.run(self.delete(url, **kwargs))
