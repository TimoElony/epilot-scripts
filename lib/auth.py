"""
Authentication utilities for Epilot API
"""

import os
from pathlib import Path
from typing import Dict

def load_env() -> None:
    """
    Load environment variables from .env file.
    Simple implementation without external dependencies.
    """
    env_file = Path(__file__).parent.parent / ".env"
    
    if not env_file.exists():
        print(f"⚠️  Warning: .env file not found at {env_file}")
        print("   Create one based on .env.example")
        return
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value

def get_auth_headers() -> Dict[str, str]:
    """
    Get authentication headers for Epilot API requests.
    """
    token = os.getenv("EPILOT_API_TOKEN", "")
    
    if not token:
        raise ValueError(
            "EPILOT_API_TOKEN not set. Please:\n"
            "1. Copy .env.example to .env\n"
            "2. Add your Epilot API token\n"
            "3. Run the script again"
        )
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
