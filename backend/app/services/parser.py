"""Resume text extraction from various file formats."""

from __future__ import annotations

import io

import structlog

logger = structlog.get_logger(__name__)


def extract_text_from_bytes(content: bytes, filename: str) -> str:
    """Extract plain text from uploaded resume file.

    Supports: .txt, .pdf, .docx
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "txt":
        return content.decode("utf-8", errors="replace")

    if ext == "pdf":
        return _extract_pdf(content)

    if ext == "docx":
        return _extract_docx(content)

    # Fallback: treat as plain text
    logger.warning("unknown_format", filename=filename, ext=ext)
    return content.decode("utf-8", errors="replace")


def _extract_pdf(content: bytes) -> str:
    """Extract text from PDF using PyPDF2."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()
    except Exception as exc:
        logger.error("pdf_extraction_failed", error=str(exc))
        return ""


def _extract_docx(content: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs).strip()
    except Exception as exc:
        logger.error("docx_extraction_failed", error=str(exc))
        return ""
