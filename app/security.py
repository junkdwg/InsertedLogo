from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import BEARER_AUTH_KEY

auth_scheme = HTTPBearer()


def validate_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> str:
    """
    Validate incoming Bearer token against configured key.
    
    Args:
        credentials: HTTP Bearer credentials from request
        
    Returns:
        The validated credentials
        
    Raises:
        HTTPException: If token is invalid
    """
    if credentials.credentials != BEARER_AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
