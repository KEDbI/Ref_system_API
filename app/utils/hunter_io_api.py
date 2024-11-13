import httpx

from fastapi import HTTPException

from app.core.config import settings

async def verify_email(email: str) -> bool:
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        try:
            if response.json()['data']['status'] == 'valid':
                return True
        except:
            raise HTTPException(status_code=503, detail='Email verifier is unavailable now. Please try later')
        return False