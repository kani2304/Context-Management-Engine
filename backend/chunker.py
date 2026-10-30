from typing import List, Tuple
from .config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_document_pages(
    file_name: str,
    pages: List[Tuple[int, str]],
    start_chunk_id: int = 1
) -> List[dict]:
    """
    Splits document pages into sliding-window text chunks.
    Window: 1000 characters.
    Overlap: 200 characters.
    """
    chunks: List[dict] = []
    current_chunk_id = start_chunk_id

    for page_num, page_text in pages:
        start = 0
        text_len = len(page_text)
        while start < text_len:
            end = min(start + CHUNK_SIZE, text_len)
            chunk_slice = page_text[start:end]
            
            # Approximate token count (words)
            token_count = len(chunk_slice.split())

            chunks.append({
                "id": current_chunk_id,
                "source": file_name,
                "page": page_num,
                "tokenCount": token_count,
                "text": chunk_slice,
            })
            current_chunk_id += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

