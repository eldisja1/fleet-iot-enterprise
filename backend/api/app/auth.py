from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import secrets

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    api_username = os.getenv("API_USERNAME")
    api_password = os.getenv("API_PASSWORD")

    if not api_username or not api_password:
        raise HTTPException(
            status_code=500,
            detail="API credentials not configured"
        )

    correct_username = secrets.compare_digest(
        credentials.username, api_username
    )
    correct_password = secrets.compare_digest(
        credentials.password, api_password
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )