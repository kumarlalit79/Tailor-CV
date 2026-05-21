import logging
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from app.schemas.resume_schema import ResumeRequest, ResumeResponse
from app.services.ats_service import ATSScoringService, get_ats_scoring_service
from app.services.openai_service import OpenAIConfigurationError, OpenAIServiceError
from app.services.pdf_service import PDFService, PDFServiceError, get_pdf_service
from app.services.resume_render_service import ResumeRenderService, get_resume_render_service
from app.services.resume_service import (
    ResumeGenerationService,
    ResumeServiceError,
    flatten_resume_content,
    get_resume_generation_service,
)
from app.utils.http_errors import (
    bad_gateway_error,
    bad_request_error,
    configuration_error,
    internal_server_error,
    not_found_error,
)

router = APIRouter(tags=["Resume"])
logger = logging.getLogger(__name__)


@router.post("/generate-resume", response_model=ResumeResponse)
async def generate_resume(
    payload: ResumeRequest,
    resume_service: ResumeGenerationService = Depends(get_resume_generation_service),
    render_service: ResumeRenderService = Depends(get_resume_render_service),
    pdf_service: PDFService = Depends(get_pdf_service),
    ats_service: ATSScoringService = Depends(get_ats_scoring_service),
) -> ResumeResponse:
    try:
        logger.info("Starting resume generation request")
        optimized_resume = await resume_service.generate_resume(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
        )
        logger.info(
            "Structured resume generated successfully. sections=%s",
            sorted(optimized_resume.keys()),
        )
        optimized_resume_text = flatten_resume_content(optimized_resume)
        ats_result = ats_service.analyze(
            resume_text=optimized_resume_text,
            job_description=payload.job_description,
        )
        logger.info(
            "ATS analysis completed. score=%s matched_count=%s missing_count=%s",
            ats_result.ats_score,
            len(ats_result.matched_keywords),
            len(ats_result.missing_keywords),
        )
        html = await run_in_threadpool(render_service.render_resume, optimized_resume)
        logger.info("Resume HTML generation completed. html_length=%s", len(html))
        pdf_path = await run_in_threadpool(
            pdf_service.generate_pdf,
            html=html,
            filename=_build_resume_file_name(optimized_resume),
        )
        logger.info("Resume PDF generated successfully. pdf_path=%s", pdf_path)

        return ResumeResponse(
            optimized_resume=optimized_resume,
            ats_score=ats_result.ats_score,
            matched_keywords=ats_result.matched_keywords,
            missing_keywords=ats_result.missing_keywords,
            pdf_url=f"/api/v1/download-resume/{pdf_path.name}",
            file_name=pdf_path.name,
        )
    except OpenAIConfigurationError as exc:
        logger.exception("Resume generation failed because OpenAI configuration is missing")
        raise configuration_error() from exc
    except ResumeServiceError as exc:
        logger.exception("Resume generation failed during structured resume validation")
        raise bad_gateway_error("Generated resume did not match the required structure.") from exc
    except OpenAIServiceError as exc:
        logger.exception("Resume generation failed during AI provider request")
        raise bad_gateway_error("Something went wrong while generating the resume.") from exc
    except PDFServiceError as exc:
        logger.exception("Resume generation failed during PDF generation")
        raise internal_server_error("Unable to generate resume PDF.") from exc
    except Exception as exc:
        logger.exception("Unexpected resume generation failure")
        raise internal_server_error("Unable to complete resume generation.") from exc


@router.get("/download-resume/{file_name}")
async def download_resume(
    file_name: str,
    pdf_service: PDFService = Depends(get_pdf_service),
) -> FileResponse:
    try:
        pdf_path = pdf_service.get_pdf_path(file_name)
    except PDFServiceError as exc:
        raise bad_request_error("Invalid resume file name.") from exc

    if not pdf_path.is_file():
        raise not_found_error("Resume PDF was not found.")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name,
        headers={"Content-Disposition": f'attachment; filename="{pdf_path.name}"'},
    )


def _build_resume_file_name(resume_data: dict[str, Any]) -> str:
    contact = resume_data.get("contact") or {}
    name = contact.get("name") if isinstance(contact, dict) else None
    base_name = name or "TailorCV_Resume"

    return f"{base_name}_Resume.pdf"
