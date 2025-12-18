from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel


router = APIRouter()


DEMO_EMAIL = "demo@pfizer.com"
DEMO_PASSWORD = "anything"


class LoginRequest(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


def _create_mock_token() -> str:
    return f"mock-{uuid.uuid4()}"


def get_current_user(authorization: Optional[str] = Header(default=None)) -> User:
    """
    Very simple dev-only auth:
    - Expects Authorization: Bearer mock-<uuid4>
    - Does not validate the UUID content beyond the prefix.
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

    return User(id="u-001", email=DEMO_EMAIL, name="Demo User")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """
    Dev-only login endpoint that checks hardcoded credentials.
    """
    if payload.email != DEMO_EMAIL or payload.password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user = User(id="u-001", email=DEMO_EMAIL, name="Demo User")
    token = _create_mock_token()
    return LoginResponse(access_token=token, token_type="bearer", user=user)


@router.get("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Return the current user if the mock token is valid.
    """
    return current_user


