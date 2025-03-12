from fastapi import  HTTPException, status, Security
import os
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key