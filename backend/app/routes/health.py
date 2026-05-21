from time import monotonic

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])
START_TIME = monotonic()


@router.get("")
async def health_check() -> dict[str, str | float]:
    return {
        "status": "ok",
        "uptime_seconds": round(monotonic() - START_TIME, 2),
    }
