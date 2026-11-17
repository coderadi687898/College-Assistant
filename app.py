"""
DocuVideo: PDF to Explainer Video Generator
Extracts contents from user's uploaded PDF using Local RAG and converts it
into an MP4 explainer video with visual slides, transitions, and audio tracks.
"""

import os
import time
from pathlib import Path
import streamlit as st

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


# Page setup
st.set_page_config(
    page_title="PDF to Explainer Video",
    page_icon="🎬",
    layout="centered"
)

# Clean, modern UI styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        margin-bottom: 24px;
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .main-header p {
        color: #94A3B8;
        font-size: 1.05rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 16px;
    }
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px 14px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎬 PDF to Explainer Video</h1>
    <p>Upload any PDF document and convert it into a presentation video with visual slides, smooth transitions, and synchronized voiceover.</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "slide_images" not in st.session_state:
    st.session_state.slide_images = []
if "video_duration" not in st.session_state:
    st.session_state.video_duration = 0.0
if "video_size_mb" not in st.session_state:
    st.session_state.video_size_mb = 0.0

# Upload section
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

col_opt1, col_opt2 = st.columns([2, 1])
with col_opt1:
    slide_count = st.slider("Number of presentation slides", min_value=3, max_value=6, value=4, step=1)
with col_opt2:
    st.write("")
    use_sample = st.button("Use Sample PDF")

pdf_source = None
file_name = "document.pdf"

if uploaded_file is not None:
    pdf_source = uploaded_file.read()
    file_name = uploaded_file.name
elif use_sample:
    sample_path = "sample_documents/sample_research_paper.pdf"
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            pdf_source = f.read()
        file_name = "sample_research_paper.pdf"
        st.info("Loaded sample research paper!")

if pdf_source:
    st.write("")
    if st.button("🚀 Generate Explainer Video", type="primary"):
        progress_bar = st.progress(0, text="Starting pipeline...")
        status = st.empty()

        try:
            # 1. Extraction
            status.info("📄 Extracting text and structure from PDF...")
            progress_bar.progress(15, text="Extracting PDF...")
            extraction = extract_pdf_content(pdf_source, file_name=file_name)

            if not extraction.full_text.strip():
                st.error("Could not extract readable text from this PDF. Please try another document.")
                st.stop()

            # 2. Local RAG Retrieval & Synthesis
            status.info("🧠 Analyzing document & extracting key concepts with RAG...")
            progress_bar.progress(35, text="Synthesizing slide deck...")
            rag = LocalRAGEngine(extraction)
            slides = rag.generate_slides(num_slides=slide_count)

            # 3. Slide Rendering
            status.info("🎨 Rendering high-definition visual presentation slides...")
            progress_bar.progress(55, text="Rendering visual slides...")
            slide_gen = SlideGenerator()
            slide_paths = slide_gen.render_deck(slides, output_dir="output/slides")
            st.session_state.slide_images = slide_paths

            # 4. Audio Narration Synthesis
            status.info("🎙️ Synthesizing voiceover audio tracks...")
            progress_bar.progress(70, text="Generating audio tracks...")
            audio_gen = AudioNarrationGenerator()
            audio_tracks = audio_gen.generate_deck_narration(slides, output_dir="output/audio")

            # 5. Video Composition & Transitions
            status.info("🎬 Assembling timeline and encoding MP4 video with transitions...")
            progress_bar.progress(85, text="Encoding MP4 video...")
            composer = VideoComposer(fps=12)
            timestamp = int(time.time())
            out_video = f"output/videos/explainer_{timestamp}.mp4"

            res = composer.compose_explainer_video(
                slide_image_paths=slide_paths,
                audio_tracks=audio_tracks,
                output_video_path=out_video
            )

            progress_bar.progress(100, text="Complete!")
            status.success(f"Video successfully created in {res.total_duration_secs}s!")

            st.session_state.video_path = res.video_path
            st.session_state.video_duration = res.total_duration_secs
            st.session_state.video_size_mb = res.file_size_mb

        except Exception as e:
            status.error(f"Error during video generation: {str(e)}")
            progress_bar.empty()

# Display Generated Video
if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.divider()
    st.subheader("📺 Generated Explainer Video")

    with open(st.session_state.video_path, "rb") as vf:
        video_bytes = vf.read()

    st.video(video_bytes)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Duration", f"{st.session_state.video_duration}s")
    with m2:
        st.metric("File Size", f"{st.session_state.video_size_mb} MB")
    with m3:
        st.metric("Slides", f"{len(st.session_state.slide_images)}")

    st.download_button(
        label="⬇️ Download MP4 Video",
        data=video_bytes,
        file_name=Path(st.session_state.video_path).name,
        mime="video/mp4",
        type="primary"
    )

    # Slide Gallery Preview
    st.divider()
    st.subheader("🖼️ Visual Slides Preview")
    if st.session_state.slide_images:
        cols = st.columns(min(len(st.session_state.slide_images), 4))
        for idx, img_p in enumerate(st.session_state.slide_images):
            col_target = cols[idx % len(cols)]
            with col_target:
                st.image(img_p, caption=f"Slide {idx + 1}", use_container_width=True)
