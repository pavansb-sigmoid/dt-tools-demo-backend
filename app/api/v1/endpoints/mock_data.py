"""
Mock data endpoints for frontend development.
All endpoints require Bearer token authentication.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api.v1.endpoints.auth import User, require_mock_auth


router = APIRouter()


@router.get("/precheck-dashboard")
def get_precheck_dashboard(
    current_user: User = Depends(require_mock_auth),
) -> Dict[str, Any]:
    """
    Return mock precheck dashboard data.
    Includes market, brand, timePeriod, KPIs, and chart placeholders.
    """
    return {
        "market": "it",
        "brand": "paxlovid",
        "timePeriod": "q4-2025",
        "kpis": {
            "totalHcps": 150,
            "totalInteractions": 450,
            "attainment": 85.5,
            "callPlanCompliance": 92.3,
        },
        "charts": {
            "segmentation": {
                "data": [
                    {"segment": "High Value", "count": 45, "percentage": 30.0},
                    {"segment": "Medium Value", "count": 75, "percentage": 50.0},
                    {"segment": "Low Value", "count": 30, "percentage": 20.0},
                ],
            },
            "frequency": {
                "data": [
                    {"frequency": "Weekly", "count": 120},
                    {"frequency": "Bi-weekly", "count": 200},
                    {"frequency": "Monthly", "count": 130},
                ],
            },
            "regionalComparison": {
                "data": [
                    {"region": "North", "value": 85.2},
                    {"region": "South", "value": 78.9},
                    {"region": "Central", "value": 92.1},
                ],
            },
        },
        "metrics": {
            "activeHcps": 142,
            "inactiveHcps": 8,
            "totalSales": 1250000,
            "averageInteractionValue": 2777.78,
        },
    }


