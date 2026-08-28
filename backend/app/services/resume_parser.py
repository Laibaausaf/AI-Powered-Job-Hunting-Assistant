"""
Extracts plain text from an uploaded resume so it can be fed into the
matching + LLM services. Supports PDF, DOCX, and plain text (6.2 bonus:
"resume parsing via a real library, not manual copy-paste").
"""
import io

from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from docx import Document


async def extract_text(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    raw = await file.read()

    if filename.endswith(".pdf"):
        return _extract_pdf(raw)
    elif filename.endswith(".docx"):
        return _extract_docx(raw)
    elif filename.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(400, "Unsupported file type. Use PDF, DOCX, or TXT.")


def _extract_pdf(raw: bytes) -> str:
    reader = PdfReader(io.BytesIO(raw))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise HTTPException(422, "Could not extract text from this PDF (it may be scanned/image-based).")
    return text


def _extract_docx(raw: bytes) -> str:
    doc = Document(io.BytesIO(raw))
    text = "\n".join(p.text for p in doc.paragraphs)
    if not text.strip():
        raise HTTPException(422, "Could not extract text from this DOCX file.")
    return text
