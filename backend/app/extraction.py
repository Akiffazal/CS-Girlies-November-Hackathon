# extraction.py
from pypdf import PdfReader
import os, math, re
from typing import List, Dict

def extract_text_from_pdf(path: str) -> List[Dict]:
    """
    Returns list of pages: [{'page_number': int, 'text': str}]
    """
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        raw = page.extract_text() or ""
        # Basic clean up
        raw = re.sub(r'\n\s+\n', '\n', raw)
        raw = raw.strip()
        pages.append({'page_number': i+1, 'text': raw})
    return pages

def chunk_text_pages(pages: List[Dict], chunk_size:int=800, overlap:int=150):
    """
    Turn pages into overlapping chunks with metadata.
    Returns list of chunks: [{'id':..., 'text':..., 'page':...}]
    """
    chunks = []
    chunk_id = 0
    for p in pages:
        words = p['text'].split()
        if not words:
            continue
        i = 0
        while i < len(words):
            chunk_words = words[i:i+chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                'id': f"p{p['page_number']}_c{chunk_id}",
                'text': chunk_text,
                'page': p['page_number']
            })
            chunk_id += 1
            i += chunk_size - overlap
    return chunks
