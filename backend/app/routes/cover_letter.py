from fastapi import APIRouter, Depends

from app.schemas.cover_letter_schema import CoverLetterRequest, CoverLetterResponse
from app.services.cover_letter_service import (
    CoverLetterService,
    CoverLetterServiceError,
    get_cover_letter_service,
)
from app.services.openai_service import OpenAIConfigurationError, OpenAIServiceError
from app.utils.http_errors import bad_gateway_error, configuration_error

router = APIRouter(tags=["Cover Letter"])


@router.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(
    payload: CoverLetterRequest,
    cover_letter_service: CoverLetterService = Depends(get_cover_letter_service),
) -> CoverLetterResponse:
    try:
        return await cover_letter_service.generate_cover_letter(
            optimized_resume=payload.optimized_resume,
            job_description=payload.job_description,
        )
    except OpenAIConfigurationError as exc:
        raise configuration_error() from exc
    except CoverLetterServiceError as exc:
        raise bad_gateway_error(
            "Generated cover letter did not match the required structure."
        ) from exc
    except OpenAIServiceError as exc:
        raise bad_gateway_error("Something went wrong while generating the cover letter.") from exc
