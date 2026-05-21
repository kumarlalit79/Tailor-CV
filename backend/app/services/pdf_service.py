from functools import lru_cache
import logging
import os
from pathlib import Path
from re import sub
from time import time
from uuid import uuid4

from app.config.settings import Settings, get_settings

BACKEND_DIR = Path(__file__).resolve().parents[2]
DEFAULT_PDF_OUTPUT_DIR = "generated/temp"
MAX_PDF_FILENAME_LENGTH = 120
logger = logging.getLogger(__name__)


class PDFServiceError(Exception):
    """Raised when PDF generation fails."""


class PDFService:
    def __init__(self, settings: Settings) -> None:
        self.output_dir = _resolve_output_dir(settings.pdf_output_dir)
        logger.debug("PDF service configured with output_dir=%s", self.output_dir)

    def generate_pdf(self, *, html: str, filename: str | None = None) -> Path:
        if not html.strip():
            logger.error("PDF generation received empty rendered HTML")
            raise PDFServiceError("Rendered HTML is required for PDF generation")

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.exception(
                "Unable to prepare PDF output directory. output_dir=%s exception_type=%s",
                self.output_dir,
                type(exc).__name__,
            )
            raise PDFServiceError("Unable to prepare PDF output directory") from exc

        output_dir_writable = os.access(self.output_dir, os.W_OK)
        pdf_filename = _build_pdf_filename(filename)
        pdf_path = self.output_dir / pdf_filename
        logger.info(
            "Starting PDF generation. output_dir=%s writable=%s pdf_path=%s html_length=%s",
            self.output_dir,
            output_dir_writable,
            pdf_path,
            len(html),
        )

        try:
            logger.debug("Importing WeasyPrint HTML renderer")
            from weasyprint import HTML

            logger.debug("Executing WeasyPrint write_pdf. base_url=%s", BACKEND_DIR)
            HTML(string=html, base_url=str(BACKEND_DIR)).write_pdf(str(pdf_path))
        except Exception as exc:
            logger.exception(
                "PDF generation failed. exception_type=%s exception_message=%s pdf_path=%s",
                type(exc).__name__,
                exc,
                pdf_path,
            )
            raise PDFServiceError("Unable to generate PDF") from exc

        if not pdf_path.is_file():
            logger.error("WeasyPrint completed without creating a PDF file. pdf_path=%s", pdf_path)
            raise PDFServiceError("PDF file was not created")

        logger.info(
            "PDF generation succeeded. pdf_path=%s file_size_bytes=%s",
            pdf_path,
            pdf_path.stat().st_size,
        )
        return pdf_path

    def get_pdf_path(self, file_name: str) -> Path:
        pdf_path = (self.output_dir / _build_pdf_filename(file_name)).resolve()
        output_dir = self.output_dir.resolve()

        if output_dir != pdf_path.parent:
            raise PDFServiceError("Invalid PDF file name")

        return pdf_path

    def cleanup_old_files(self, *, max_age_seconds: int = 1_800) -> int:
        if not self.output_dir.exists():
            return 0

        removed_count = 0
        cutoff = time() - max_age_seconds

        for pdf_path in self.output_dir.glob("*.pdf"):
            if pdf_path.is_file() and pdf_path.stat().st_mtime < cutoff:
                pdf_path.unlink()
                removed_count += 1

        return removed_count


def _build_pdf_filename(filename: str | None) -> str:
    base_name = filename.strip() if filename else f"resume_{uuid4().hex}"
    safe_name = sub(r"[^A-Za-z0-9_.-]+", "_", base_name).strip("._")

    if not safe_name:
        safe_name = f"resume_{uuid4().hex}"

    if not safe_name.lower().endswith(".pdf"):
        safe_name = f"{safe_name}.pdf"

    if len(safe_name) > MAX_PDF_FILENAME_LENGTH:
        stem = safe_name[:-4]
        safe_name = f"{stem[: MAX_PDF_FILENAME_LENGTH - 4]}.pdf"

    return safe_name


def _resolve_output_dir(output_dir: str | None) -> Path:
    configured_dir = Path(output_dir or DEFAULT_PDF_OUTPUT_DIR)

    if not configured_dir.is_absolute():
        configured_dir = BACKEND_DIR / configured_dir

    return configured_dir


@lru_cache
def get_pdf_service() -> PDFService:
    return PDFService(settings=get_settings())
