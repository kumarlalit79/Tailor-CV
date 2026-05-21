from collections.abc import Sequence

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routes import ats, cold_email, cover_letter, health, resume

API_V1_PREFIX = "/api/v1"


def _include_api_routes(app: FastAPI) -> None:
    api_router = APIRouter(prefix=API_V1_PREFIX)
    route_modules: Sequence[APIRouter] = (
        health.router,
        resume.router,
        ats.router,
        cover_letter.router,
        cold_email.router,
    )

    for router in route_modules:
        api_router.include_router(router)

    app.include_router(api_router)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="TailorCV API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _include_api_routes(app)

    return app


app = create_app()
