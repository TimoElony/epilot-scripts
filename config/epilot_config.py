"""
Epilot API Configuration

This file contains base URLs and configuration for all Epilot APIs.
Update your authentication settings in the .env file.
"""

import os
from typing import Dict

# Base URL for Epilot API discovery
EPILOT_DISCOVERY_URL = "https://docs.epilot.io/openapi-specs/apis.json"

# Common Epilot API Base URLs
# These are loaded dynamically but commonly used ones are listed here for reference
EPILOT_API_URLS: Dict[str, str] = {
    "entity": "https://entity.sls.epilot.io",
    "user": "https://user.sls.epilot.io",
    "customer": "https://customer.sls.epilot.io",
    "order": "https://order.sls.epilot.io",
    "product": "https://product.sls.epilot.io",
    "pricing": "https://pricing.sls.epilot.io",
    "workflow": "https://workflow-definition.sls.epilot.io",
    "message": "https://message.sls.epilot.io",
    "file": "https://file.sls.epilot.io",
    "organization": "https://organization.sls.epilot.io",
}

# Authentication
def get_auth_token() -> str:
    """
    Get authentication token from environment variable.
    Set EPILOT_API_TOKEN in your .env file.
    """
    token = os.getenv("EPILOT_API_TOKEN", "")
    if not token:
        raise ValueError(
            "EPILOT_API_TOKEN not found. Please set it in your .env file."
        )
    return token

def get_auth_headers() -> Dict[str, str]:
    """
    Get standard authentication headers for Epilot API calls.
    """
    return {
        "Authorization": f"Bearer {get_auth_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# Request configuration
DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
