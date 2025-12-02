#!/usr/bin/env python3
"""
Create Epilot Design

Creates a new design in the Epilot Design Builder API with custom styling.

Usage:
    python scripts/designs/create_design.py --name "My Design"
    python scripts/designs/create_design.py --config designs/green_theme_config.json
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path
from typing import Dict, Any

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

DESIGN_API_BASE = "https://design-builder-api.sls.epilot.io"

def create_green_theme_design(name: str = "Green Modern Theme") -> Dict[str, Any]:
    """
    Create a design configuration with green theme, Roboto + Montserrat fonts,
    and blueish white backgrounds.
    
    Args:
        name: Name for the design
    
    Returns:
        Design configuration object
    """
    return {
        "design": {
            "style_name": name,
            "style": {
                "logo": {
                    "main": {
                        "name": "",
                        "url": "",
                        "s3_object_key": ""
                    }
                },
                "typography": {
                    "primary": "#1f2937FF",  # Near black for primary text
                    "secondary": "#6b7280FF",  # Neutral gray for secondary text
                    "font": {
                        "font_id": "Roboto",
                        "font_family": "Roboto",
                        "font_name": "Roboto",
                        "font_weight_regular": "400",
                        "font_weight_medium": "500",
                        "font_weight_bold": "700",
                        "urls": [
                            {
                                "type": "WOFF",
                                "url": "https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Mu4mxK.woff2"
                            }
                        ]
                    }
                },
                "palette": {
                    "primary": "#16a34aFF",  # Tailwind green-600
                    "secondary": "#15803dFF",  # Tailwind green-700
                    "navbar": "#16a34aFF",  # Green navbar for brand consistency
                    "background": "#f8f9fbFF",  # Slightly blueish white
                    "paper": "#fafbfcFF",  # Lighter blueish white for cards
                    "error": "#dc2626FF"  # Tailwind red-600
                },
                "consumer": {
                    "widgets": [],
                    "customer_portals": []
                }
            }
        }
    }

async def create_design(client: EpilotClient, design_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new design via the API.
    
    Args:
        client: EpilotClient instance
        design_config: Design configuration object
    
    Returns:
        Created design object with ID
    """
    print(f"📝 Creating design: {design_config.get('style_name', 'Untitled')}...")
    
    try:
        url = f"{DESIGN_API_BASE}/v1/designs"
        result = await client.post(url, data=design_config)
        
        design_id = result.get('id', result.get('_id', 'unknown'))
        print(f"✅ Design created successfully!")
        print(f"   ID: {design_id}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error creating design: {e}")
        import traceback
        traceback.print_exc()
        raise

async def main(name: str, config_file: str = None):
    """
    Main function to create a design.
    
    Args:
        name: Name for the design
        config_file: Optional path to JSON config file
    """
    load_env()
    client = EpilotClient()
    
    print("🎨 Creating new Epilot design...\n")
    
    try:
        if config_file:
            # Load from config file
            with open(config_file, 'r') as f:
                design_config = json.load(f)
            print(f"📄 Loaded configuration from {config_file}")
        else:
            # Use green theme
            design_config = create_green_theme_design(name)
            print("🌿 Using Green Modern Theme configuration")
        
        # Create the design
        result = await create_design(client, design_config)
        
        # Save the created design locally
        output_dir = Path("data/output/designs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        design_id = result.get('id', result.get('_id', 'unknown'))
        output_file = output_dir / f"design_{design_id}_created.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Design saved locally to: {output_file}")
        print("\n🎉 Design creation complete!")
        
    except Exception as e:
        print(f"\n❌ Failed to create design: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Epilot design")
    parser.add_argument(
        "--name",
        default="Green Modern Theme",
        help="Name for the design"
    )
    parser.add_argument(
        "--config",
        help="Path to JSON configuration file (optional)"
    )
    
    args = parser.parse_args()
    
    asyncio.run(main(args.name, args.config))
