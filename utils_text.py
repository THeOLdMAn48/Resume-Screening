# src/utils_text.py
import re
from typing import Union
from io import BytesIO

# pypdf import
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except Exception:
    PYPDF_AVAILABLE = False

def clean_text(text: str) -> str:
    """Lowercase, remove extra whitespace and most punctuation (keep #,+ for skills)."""
    if not isinstance(text, str):
        return ""
    txt = text.lower()
    txt = re.sub(r'\r\n', ' ', txt)
    txt = re.sub(r'\n', ' ', txt)
    txt = re.sub(r'[^a-z0-9\s\+\#\-\_\.]', ' ', txt)  # keep some useful tokens
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

def extract_text_from_pdf_file(file_like: Union[str, bytes, BytesIO]) -> str:
    """
    Accepts file path or bytes (as returned by streamlit file_uploader).
    Returns extracted text or empty string if extraction fails.
    """
    if not PYPDF_AVAILABLE:
        return ""
    try:
        if isinstance(file_like, (bytes, bytearray)):
            stream = BytesIO(file_like)
            reader = PdfReader(stream)
        else:
            reader = PdfReader(file_like)
        pages = []
        for p in reader.pages:
            text = p.extract_text()
            if text:
                pages.append(text)
        return " ".join(pages)
    except Exception:
        return ""

def read_text_file(file_like: Union[str, bytes]) -> str:
    """Read text from bytes or file path."""
    try:
        if isinstance(file_like, (bytes, bytearray)):
            return file_like.decode('utf-8', errors='ignore')
        else:
            with open(file_like, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception:
        return ""
