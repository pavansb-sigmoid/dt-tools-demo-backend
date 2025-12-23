from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel


router = APIRouter()


DEMO_EMAIL = "demo@pfizer.com"


class LoginRequest(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


def _create_mock_token() -> str:
    return f"mock-{uuid.uuid4()}"


def require_mock_auth(authorization: Optional[str] = Header(default=None)) -> User:
    """
    Reusable dependency for mock Bearer token authentication.
    Expects Authorization: Bearer mock-<uuid4>
    Returns User if valid, raises 401 otherwise.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token or not token.startswith("mock-"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return User(email=DEMO_EMAIL, name="Demo User")


# Alias for backward compatibility
get_current_user = require_mock_auth


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """
    Dev-only login endpoint that checks hardcoded email and accepts any non-empty password.
    """
    if payload.email != DEMO_EMAIL or not payload.password or not payload.password.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user = User(email=DEMO_EMAIL, name="Demo User")
    token = _create_mock_token()
    return LoginResponse(access_token=token, token_type="bearer", user=user)


@router.get("/me", response_model=User)
def read_me(current_user: User = Depends(require_mock_auth)) -> User:
    """
    Return the current user if the mock token is valid.
    """
    return current_user


