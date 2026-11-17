"""
PDF Content Extractor Module
Extracts clean text, pages, and metadata from uploaded PDF documents.
"""

import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union
import pdfplumber
import pypdfium2 as pdfium


@dataclass
class PageContent:
    page_number: int
    text: str
    word_count: int


@dataclass
class DocumentMetadata:
    title: str
    page_count: int
    word_count: int
    file_name: str


@dataclass
class PDFExtractionResult:
    metadata: DocumentMetadata
    pages: List[PageContent]
    full_text: str


def clean_text(raw_text: str) -> str:
    """Repairs hyphenated linebreaks, removes extraneous whitespace and blank lines."""
    if not raw_text:
        return ""
    # Repair hyphenated word breaks (e.g. "com- \n puter" -> "computer")
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', raw_text)
    # Normalize spaces
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    # Remove standalone page numbers
    cleaned_lines = [l for l in lines if not re.match(r'^(page\s+\d+(\s+of\s+\d+)?|\d+)$', l, re.IGNORECASE)]
    text = '\n'.join(cleaned_lines)
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def infer_title(first_page_text: str, default_filename: str) -> str:
    """Extracts a readable title from the first non-empty lines of the document."""
    if not first_page_text:
        return Path(default_filename).stem.replace("_", " ").title()
    for line in first_page_text.split('\n'):
        line = line.strip()
        if 5 <= len(line) <= 100 and not line.lower().startswith(("page ", "http", "www")):
            return line
    return Path(default_filename).stem.replace("_", " ").title()


def extract_pdf_content(
    source: Union[str, Path, bytes, io.BytesIO],
    file_name: str = "document.pdf"
) -> PDFExtractionResult:
    """Extracts text and metadata from a PDF file path or bytes."""
    if isinstance(source, (str, Path)):
        p = Path(source)
        file_name = p.name
        pdf_file = str(p)
    elif isinstance(source, bytes):
        pdf_file = io.BytesIO(source)
    else:
        pdf_file = source

    pages: List[PageContent] = []
    full_text_parts: List[str] = []

    # Primary extraction via pdfplumber
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for idx, page in enumerate(pdf.pages, start=1):
                raw = page.extract_text() or ""
                cleaned = clean_text(raw)
                if cleaned:
                    pages.append(PageContent(page_number=idx, text=cleaned, word_count=len(cleaned.split())))
                    full_text_parts.append(cleaned)
    except Exception:
        # Fallback to pypdfium2
        pages.clear()
        full_text_parts.clear()
        if isinstance(pdf_file, io.BytesIO):
            pdf_file.seek(0)
        doc = pdfium.PdfDocument(pdf_file)
        for idx in range(len(doc)):
            raw = doc[idx].get_textpage().get_text_range()
            cleaned = clean_text(raw)
            if cleaned:
                pages.append(PageContent(page_number=idx + 1, text=cleaned, word_count=len(cleaned.split())))
                full_text_parts.append(cleaned)

    full_text = "\n\n".join(full_text_parts)
    title = infer_title(pages[0].text if pages else "", file_name)
    total_words = sum(p.word_count for p in pages)

    metadata = DocumentMetadata(
        title=title,
        page_count=len(pages),
        word_count=total_words,
        file_name=file_name
    )

    return PDFExtractionResult(
        metadata=metadata,
        pages=pages,
        full_text=full_text
    )
