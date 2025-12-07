#!/usr/bin/env python3
"""
Analyze Epilot Entity Schemas for Infrastructure Project Use Cases

Checks which entity types exist and which support workflows.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.auth import load_env
from lib.api_client import EpilotClient

async def analyze_schemas():
    load_env()
    client = EpilotClient()
    
    url = 'https://entity.sls.epilot.io/v1/entity/schemas'
    result = await client.get(url)
    
    schemas = result.get('schemas', [])
    
    print(f'📊 Total entity schemas: {len(schemas)}\n')
    print('=' * 80)
    
    # Categorize
    crm_entities = []
    operational_entities = []
    project_like = []
    
    for schema in schemas:
        slug = schema.get('slug', '')
        name = schema.get('name', '')
        caps = schema.get('capabilities', [])
        has_workflow = any(c.get('name') == 'workflow' for c in caps)
        
        entry = f"{slug:30} {name:40} {'✓ Workflow' if has_workflow else ''}"
        
        if any(word in slug for word in ['contact', 'account', 'lead', 'campaign']):
            crm_entities.append(entry)
        elif any(word in slug for word in ['opportunity', 'order', 'contract', 'submission']):
            operational_entities.append(entry)
        elif any(word in slug for word in ['ticket', 'task', 'project']):
            project_like.append(entry)
        else:
            if 'product' not in slug and 'price' not in slug:
                project_like.append(entry)
    
    print('\n🤝 CRM Entities:')
    for e in crm_entities:
        print(f'  {e}')
    
    print('\n\n📦 Operational/Transactional Entities:')
    for e in operational_entities:
        print(f'  {e}')
    
    print('\n\n🎯 Potentially Useful for Infrastructure Projects:')
    for e in project_like[:15]:
        print(f'  {e}')
    
    print('\n' + '=' * 80)
    print('\n💡 RECOMMENDATIONS FOR AUSBAU GLASFASER:\n')
    print('Based on your need for admin-initiated infrastructure processes:\n')
    print('1. ⭐ TICKET entity')
    print('   - Generic "work item" concept')
    print('   - Has workflow capability')
    print('   - Not tied to customer/sales')
    print('   - Use for: Internal projects, infrastructure work')
    print()
    print('2. ⭐⭐ ORDER entity (your current fallback)')
    print('   - Already using for Tarifabschluss')
    print('   - Has workflow capability')
    print('   - Can exist without customer')
    print('   - Use type="infrastructure" to distinguish')
    print()
    print('3. ❌ OPPORTUNITY (what you\'re doing now)')
    print('   - Semantically wrong for non-sales projects')
    print('   - Pollutes sales pipeline')
    print('   - Should avoid')

asyncio.run(analyze_schemas())
