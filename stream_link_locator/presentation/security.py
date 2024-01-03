from http import HTTPStatus

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

from config import settings


def get_api_key(api_key_header: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
    """Get and validate API Key"""
    if api_key_header in settings.api_keys:
        return api_key_header
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
