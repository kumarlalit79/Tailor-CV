from fastapi import APIRouter, Depends

from app.schemas.cold_email_schema import ColdEmailRequest, ColdEmailResponse
from app.services.cold_email_service import (
    ColdEmailService,
    ColdEmailServiceError,
    get_cold_email_service,
)
from app.services.openai_service import OpenAIConfigurationError, OpenAIServiceError
from app.utils.http_errors import bad_gateway_error, configuration_error

router = APIRouter(tags=["Cold Email"])


@router.post("/generate-cold-email", response_model=ColdEmailResponse)
async def generate_cold_email(
    payload: ColdEmailRequest,
    cold_email_service: ColdEmailService = Depends(get_cold_email_service),
) -> ColdEmailResponse:
    try:
        return await cold_email_service.generate_cold_email(
            optimized_resume=payload.optimized_resume,
            job_description=payload.job_description,
        )
    except OpenAIConfigurationError as exc:
        raise configuration_error() from exc
    except ColdEmailServiceError as exc:
        raise bad_gateway_error("Generated cold email did not match the required structure.") from exc
    except OpenAIServiceError as exc:
        raise bad_gateway_error("Something went wrong while generating the cold email.") from exc
