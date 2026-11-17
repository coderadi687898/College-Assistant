"""
Command-Line Interface (CLI) for PDF to Explainer Video Converter
Usage:
    python cli.py --pdf sample_documents/sample_research_paper.pdf --slides 4 --output output/videos/my_video.mp4
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from core.pdf_extractor import extract_pdf_content
from core.rag_engine import LocalRAGEngine
from core.slide_generator import SlideGenerator
from core.audio_generator import AudioNarrationGenerator
from core.video_composer import VideoComposer


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Convert PDF to Explainer Video")
    parser.add_argument(
        "--pdf",
        type=str,
        default="sample_documents/sample_research_paper.pdf",
        help="Path to input PDF document."
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=4,
        choices=[3, 4, 5, 6],
        help="Number of slides (3 to 6)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/videos/cli_explainer.mp4",
        help="Output path for the generated MP4 video."
    )

    args = parser.parse_args()
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"[-] Error: File not found at '{pdf_path}'")
        sys.exit(1)

    print("=" * 60)
    print("[+] PDF TO EXPLAINER VIDEO CONVERTER")
    print("=" * 60)
    print(f"[*] Input PDF:       {pdf_path.name}")
    print(f"[*] Target Slides:   {args.slides}")
    print(f"[*] Output Path:     {args.output}")
    print("-" * 60)

    start_total = time.time()

    # 1. Extraction
    print("\n[1/4] Extracting text from PDF...")
    extraction = extract_pdf_content(str(pdf_path))
    print(f"      Title: '{extraction.metadata.title}' ({extraction.metadata.page_count} pages, {extraction.metadata.word_count} words)")

    # 2. Local RAG Retrieval & Synthesis
    print("\n[2/4] Retrieving key concepts using Local RAG...")
    rag = LocalRAGEngine(extraction)
    slides = rag.generate_slides(num_slides=args.slides)
    for s in slides:
        print(f"      -> Slide {s.slide_index}: [{s.category}] {s.title}")

    # 3. Slide Rendering
    print("\n[3/4] Rendering 1080p visual slides...")
    slide_gen = SlideGenerator()
    slide_paths = slide_gen.render_deck(slides, output_dir="output/slides")

    # 4. Audio Synthesis
    print("\n[4/4] Synthesizing narration audio tracks & encoding video...")
    audio_gen = AudioNarrationGenerator()
    audio_tracks = audio_gen.generate_deck_narration(slides, output_dir="output/audio")

    # 5. Video Composition with transitions
    composer = VideoComposer(fps=12)
    res = composer.compose_explainer_video(
        slide_image_paths=slide_paths,
        audio_tracks=audio_tracks,
        output_video_path=args.output
    )

    total_elapsed = time.time() - start_total
    print("\n" + "=" * 60)
    print("[+] VIDEO GENERATION COMPLETE!")
    print("=" * 60)
    print(f"[*] Final MP4:       {os.path.abspath(res.video_path)}")
    print(f"[*] Duration:        {res.total_duration_secs}s")
    print(f"[*] File Size:       {res.file_size_mb} MB")
    print(f"[*] Total Time:      {total_elapsed:.1f}s")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
