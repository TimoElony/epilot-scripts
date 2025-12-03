import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('EPILOT_API_TOKEN')

async def check():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://entity.sls.epilot.io/v1/entity/opportunity/fbd55a8d-e83e-4190-8d23-29f363858d0f',
            headers={'Authorization': f'Bearer {token}'}
        )
        opp = response.json()
        print(f"Current status value: '{opp.get('status')}'")
        print(f"Title: {opp.get('_title')}")

asyncio.run(check())
