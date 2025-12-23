"""
Metadata endpoints for dropdown values (markets, brands, time periods).
All endpoints require mock Bearer token authentication.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.v1.endpoints.auth import User, require_mock_auth
from app.services import metadata_store


router = APIRouter()


@router.get("/markets")
def list_markets(
    current_user: User = Depends(require_mock_auth),
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Return all available markets.
    """
    return metadata_store.get_markets()


@router.get("/brands")
def list_brands(
    marketId: Optional[str] = Query(default=None, alias="marketId"),
    current_user: User = Depends(require_mock_auth),
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Return all brands, optionally filtered by marketId.
    """
    brands_data = metadata_store.get_brands()
    items = brands_data["items"]

    if marketId:
        items = [b for b in items if b.get("marketId") == marketId]

    return {"items": items}


@router.get("/time-periods")
def list_time_periods(
    current_user: User = Depends(require_mock_auth),
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Return all available time periods.
    """
    return metadata_store.get_time_periods()

