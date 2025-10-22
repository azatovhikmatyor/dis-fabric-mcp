from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import Environment

import pandas as pd

security = HTTPBearer()
env = Environment() # type: ignore

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials.credentials != env.mcp_auth_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid or expired token',
        )
    return credentials.credentials

