import io
from typing import List, Tuple
import pymupdf
from PIL import Image

def extract_text_from_file(file_name: str, file_bytes: bytes) -> List[Tuple[int, str]]:
    """
    Extracts pages with page numbers from PDF documents or images.
    Returns: List of (page_number, page_text) tuples.
    """
    lower_name = file_name.lower()
    pages: List[Tuple[int, str]] = []

    if lower_name.endswith(".pdf"):
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        for page_idx in range(len(doc)):
            page_text = doc[page_idx].get_text("text").strip()
            if page_text:
                pages.append((page_idx + 1, page_text))
        doc.close()

    elif lower_name.endswith((".png", ".jpg", ".jpeg")):
        try:
            import pytesseract
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image).strip()
            if text:
                pages.append((1, text))
        except Exception as e:
            print(f"[Extractor Warning] OCR failed for {file_name}: {e}")

    return pages

