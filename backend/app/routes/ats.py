from fastapi import APIRouter, Depends

from app.schemas.ats_schema import ATSRequest, ATSResponse
from app.services.ats_service import ATSScoringService, get_ats_scoring_service
from app.utils.http_errors import internal_server_error

router = APIRouter(tags=["ATS"])


@router.post("/generate-ats-score", response_model=ATSResponse)
async def generate_ats_score(
    payload: ATSRequest,
    ats_service: ATSScoringService = Depends(get_ats_scoring_service),
) -> ATSResponse:
    try:
        return ats_service.analyze(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
        )
    except Exception as exc:
        raise internal_server_error("Unable to generate ATS score.") from exc
