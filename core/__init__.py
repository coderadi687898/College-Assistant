"""
Core package for DocuVideo RAG Engine.
Includes PDF extraction, RAG indexing & retrieval, slide rendering,
voiceover synthesis, and video composition.
"""

from .pdf_extractor import extract_pdf_content, PDFExtractionResult, DocumentMetadata
from .rag_engine import LocalRAGEngine, SlideContent
from .slide_generator import SlideGenerator
from .audio_generator import AudioNarrationGenerator
from .video_composer import VideoComposer

__all__ = [
    "extract_pdf_content",
    "PDFExtractionResult",
    "DocumentMetadata",
    "LocalRAGEngine",
    "SlideContent",
    "SlideGenerator",
    "AudioNarrationGenerator",
    "VideoComposer",
]
