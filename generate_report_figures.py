import os
from PIL import Image, ImageDraw, ImageFont

out_dir = r"d:\Projects\Minor Project\College Assistant\report_assets\figures"
os.makedirs(out_dir, exist_ok=True)

font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
title_font = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 28)
heading_font = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 20)
sub_font = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 16)
body_font = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 15)
small_font = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 13)

def draw_rounded_card(draw, box, fill, outline, width=2, radius=12):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color="#475569", width=3, arrow_size=10):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=color)

# -------------------------------------------------------------
# Figure 1: High-Level End-to-End System Architecture
# -------------------------------------------------------------
def create_fig1():
    img = Image.new("RGB", (1400, 750), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1400, 60], fill="#0F172A")
    draw.text((30, 16), "DocuVideo RAG: High-Level End-to-End System Architecture", font=title_font, fill="#FFFFFF")
    
    # 5 Major Layer Columns / Stages
    stages = [
        ("1. Ingestion Layer", "#EFF6FF", "#3B82F6", [
            ("User PDF Upload", "Streamlit UI / CLI"),
            ("Document Parsing", "pdfplumber & pypdfium2"),
            ("Text Normalization", "Regex cleanup & ligatures")
        ]),
        ("2. RAG Indexing Layer", "#F0FDF4", "#10B981", [
            ("Sliding Window", "450 char win, 75 overlap"),
            ("Metadata Tagging", "Page provenance & index"),
            ("Vector Storage", "ChromaDB (MiniLM) / TF-IDF")
        ]),
        ("3. Salience & Synthesis", "#FAF5FF", "#A855F7", [
            ("Thematic Queries", "5 Slide aspects defined"),
            ("Vector Retrieval", "Top-K nearest neighbors"),
            ("TextRank Salience", "Novelty filter & scoring")
        ]),
        ("4. Media Generation", "#FFF7ED", "#F97316", [
            ("Visual Renderer", "Pillow 1080p slide cards"),
            ("Audio Synthesizer", "Windows SAPI5 offline"),
            ("Wave Timing Analyser", "Exact millisecond duration")
        ]),
        ("5. Video Multiplexing", "#FDF2F8", "#EC4899", [
            ("Timeline Alignment", "Slide matched to audio"),
            ("Crossfade Transitions", "0.5s visual blend"),
            ("H.264 / AAC Encoding", "Broadcast MP4 at 12 FPS")
        ]),
    ]
    
    col_w = 230
    gap = 40
    start_x = 45
    
    for i, (stage_title, bg_col, border_col, items) in enumerate(stages):
        x = start_x + i * (col_w + gap)
        # Main Column Container
        draw_rounded_card(draw, [x, 90, x + col_w, 680], "#FFFFFF", border_col, width=2, radius=14)
        
        # Stage Header
        draw.rounded_rectangle([x, 90, x + col_w, 140], radius=14, fill=bg_col)
        draw.rectangle([x, 125, x + col_w, 140], fill=bg_col) # flatten bottom
        draw.text((x + 12, 105), stage_title, font=sub_font, fill=border_col)
        
        # Items
        item_y = 160
        for title, sub in items:
            draw_rounded_card(draw, [x + 10, item_y, x + col_w - 10, item_y + 130], bg_col, border_col, width=1, radius=8)
            draw.text((x + 20, item_y + 15), title, font=sub_font, fill="#0F172A")
            draw.text((x + 20, item_y + 45), sub, font=small_font, fill="#475569")
            
            # Indicator dot
            draw.ellipse([x + col_w - 30, item_y + 20, x + col_w - 20, item_y + 30], fill=border_col)
            item_y += 150
            
        # Draw Arrow to next stage
        if i < len(stages) - 1:
            arrow_start = (x + col_w + 5, 380)
            arrow_end = (x + col_w + gap - 5, 380)
            draw_arrow(draw, arrow_start, arrow_end, color="#64748B", width=3, arrow_size=10)
            
    img.save(os.path.join(out_dir, "fig1_system_architecture.png"))
    print("Created fig1_system_architecture.png")

# -------------------------------------------------------------
# Figure 2: Document Ingestion and Chunking Strategy
# -------------------------------------------------------------
def create_fig2():
    img = Image.new("RGB", (1300, 600), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1300, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 2: Text Normalization and Context-Preserving Sliding Window Chunking", font=title_font, fill="#FFFFFF")
    
    # Raw PDF Document representation
    draw_rounded_card(draw, [50, 90, 320, 530], "#FFFFFF", "#94A3B8", width=2, radius=10)
    draw.text((80, 110), "Uploaded PDF Document", font=heading_font, fill="#1E293B")
    draw.text((80, 145), "- Multi-page raw layout\n- Headers, footers & ligatures\n- Hyphenated line breaks", font=body_font, fill="#64748B")
    draw.rectangle([70, 240, 300, 480], fill="#F1F5F9", outline="#CBD5E1")
    draw.text((85, 260), "Document Stream:\nPage 1: Title & Abstract...\nPage 2: Methodology...\nPage 3: Evaluation...", font=small_font, fill="#334155")
    
    # Arrow 1
    draw_arrow(draw, (330, 310), (410, 310), color="#2563EB", width=3)
    
    # Cleaning Module
    draw_rounded_card(draw, [420, 140, 720, 480], "#EFF6FF", "#3B82F6", width=2, radius=12)
    draw.text((450, 165), "Text Cleanup & Normalization", font=heading_font, fill="#1E40AF")
    draw.text((450, 215), "1. Reconstruct broken words (e.g. con-\n   figuration -> configuration)\n2. Normalize Unicode ligature glyphs\n3. Strip repetitive running headers\n4. Retain page numbering provenance", font=body_font, fill="#1E293B")
    
    # Arrow 2
    draw_arrow(draw, (730, 310), (810, 310), color="#2563EB", width=3)
    
    # Chunking Visualization
    draw_rounded_card(draw, [820, 90, 1250, 530], "#FFFFFF", "#10B981", width=2, radius=12)
    draw.text((850, 110), "Sliding Window Chunks", font=heading_font, fill="#065F46")
    
    # Chunk 1
    draw_rounded_card(draw, [840, 160, 1220, 240], "#ECFDF5", "#059669", width=1, radius=8)
    draw.text((860, 175), "Chunk #0 (Length: 450 chars | Page: 1)", font=sub_font, fill="#047857")
    draw.text((860, 205), "...scalable decentralized edge architectures require low latency...", font=small_font, fill="#334155")
    
    # Overlap indicator
    draw.rectangle([980, 235, 1150, 275], fill="#FEF3C7", outline="#F59E0B")
    draw.text((995, 245), "Overlap = 75 chars", font=small_font, fill="#B45309")
    
    # Chunk 2
    draw_rounded_card(draw, [840, 270, 1220, 350], "#ECFDF5", "#059669", width=1, radius=8)
    draw.text((860, 285), "Chunk #1 (Length: 450 chars | Page: 1)", font=sub_font, fill="#047857")
    draw.text((860, 315), "...require low latency. In this paper, we propose a lightweight...", font=small_font, fill="#334155")
    
    # Chunk 3
    draw_rounded_card(draw, [840, 380, 1220, 460], "#ECFDF5", "#059669", width=1, radius=8)
    draw.text((860, 395), "Chunk #2 (Length: 450 chars | Page: 2)", font=sub_font, fill="#047857")
    draw.text((860, 425), "...benchmarking shows 42% throughput gain across clusters...", font=small_font, fill="#334155")
    
    draw.text((850, 485), "Metadata Tag: {chunk_id: N, page_num: P, token_count: C}", font=small_font, fill="#475569")
    
    img.save(os.path.join(out_dir, "fig2_chunking_pipeline.png"))
    print("Created fig2_chunking_pipeline.png")

# -------------------------------------------------------------
# Figure 3: Dual-Mode Vector Retrieval Architecture
# -------------------------------------------------------------
def create_fig3():
    img = Image.new("RGB", (1300, 650), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1300, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 3: Dual-Mode Vector Space Retrieval (ChromaDB ONNX vs. TF-IDF)", font=title_font, fill="#FFFFFF")
    
    # Query input
    draw_rounded_card(draw, [50, 260, 280, 390], "#EFF6FF", "#2563EB", width=2, radius=12)
    draw.text((70, 280), "Thematic Aspect Query", font=heading_font, fill="#1E40AF")
    draw.text((70, 320), 'q = "System Architecture\nand Core Methodology"', font=sub_font, fill="#334155")
    
    # Branching arrows
    draw_arrow(draw, (285, 300), (390, 180), color="#2563EB", width=3)
    draw_arrow(draw, (285, 350), (390, 470), color="#059669", width=3)
    
    # Mode A: ChromaDB Dense ONNX
    draw_rounded_card(draw, [400, 90, 900, 280], "#FFFFFF", "#2563EB", width=2, radius=12)
    draw.rounded_rectangle([400, 90, 900, 130], radius=12, fill="#DBEAFE")
    draw.rectangle([400, 115, 900, 130], fill="#DBEAFE")
    draw.text((420, 100), "Mode A: Dense Semantic Embeddings (ChromaDB)", font=sub_font, fill="#1E40AF")
    draw.text((420, 145), "- Embedding Engine: all-MiniLM-L6-v2 ONNX Runtime (CPU)\n- Embedding Dimensionality: d = 384 continuous dimensions\n- Index Structure: Hierarchical Navigable Small World (HNSW)\n- Metric: L2 / Cosine Distance in Euclidean embedding space", font=body_font, fill="#1E293B")
    
    # Mode B: Sparse TF-IDF Cosine
    draw_rounded_card(draw, [400, 380, 900, 570], "#FFFFFF", "#059669", width=2, radius=12)
    draw.rounded_rectangle([400, 380, 900, 420], radius=12, fill="#D1FAE5")
    draw.rectangle([400, 405, 900, 420], fill="#D1FAE5")
    draw.text((420, 390), "Mode B: Pure Sparse Vector Retrieval (TF-IDF)", font=sub_font, fill="#065F46")
    draw.text((420, 435), "- Term Weight: TF(t, d) * IDF(t, D) with logarithmic smoothing\n- Space: High-dimensional sparse vocabulary matrix\n- Ranking Metric: Exact Cosine Similarity dot product\n- 100% Deterministic & Zero Model Weight Footprint", font=body_font, fill="#1E293B")
    
    # Joining arrows to Top-K
    draw_arrow(draw, (905, 185), (990, 300), color="#2563EB", width=3)
    draw_arrow(draw, (905, 475), (990, 350), color="#059669", width=3)
    
    # Ranked Output Chunks
    draw_rounded_card(draw, [1000, 170, 1260, 480], "#FAF5FF", "#A855F7", width=2, radius=12)
    draw.text((1020, 190), "Top-K Retrieved Chunks", font=heading_font, fill="#6B21A8")
    draw.text((1020, 240), "Rank 1: Chunk #4 (Score: 0.88)\nRank 2: Chunk #12 (Score: 0.81)\nRank 3: Chunk #2 (Score: 0.74)", font=body_font, fill="#334155")
    draw.rectangle([1020, 340, 1240, 450], fill="#FFFFFF", outline="#D8B4FE")
    draw.text((1035, 355), "Grounding Provenance:\nPage IDs: [1, 2, 4]\nPassed to TextRank\nSalience Selector", font=small_font, fill="#581C87")
    
    img.save(os.path.join(out_dir, "fig3_retrieval_comparison.png"))
    print("Created fig3_retrieval_comparison.png")

# -------------------------------------------------------------
# Figure 4: TextRank Salience Scoring and Novelty Filtering
# -------------------------------------------------------------
def create_fig4():
    img = Image.new("RGB", (1300, 620), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1300, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 4: Extractive TextRank Salience Scoring and Novelty Filtering Workflow", font=title_font, fill="#FFFFFF")
    
    # Box 1: Input Candidate Sentences
    draw_rounded_card(draw, [50, 100, 350, 550], "#FFFFFF", "#3B82F6", width=2, radius=12)
    draw.text((70, 120), "Candidate Sentences", font=heading_font, fill="#1E40AF")
    draw.text((70, 155), "Extracted from Top-K\nRetrieved Passages", font=small_font, fill="#64748B")
    
    sentences = [
        "S1: Edge computing achieves...",
        "S2: Experimental tests show 42%...",
        "S3: Latency dropped by 18ms...",
        "S4: Edge computing achieves...",
        "S5: The proposed broker model..."
    ]
    y = 210
    for s in sentences:
        draw_rounded_card(draw, [65, y, 335, y + 50], "#EFF6FF", "#BFDBFE", width=1, radius=6)
        draw.text((75, y + 15), s, font=small_font, fill="#1E293B")
        y += 65
        
    draw_arrow(draw, (355, 325), (435, 325), color="#3B82F6", width=3)
    
    # Box 2: Salience Scoring Function
    draw_rounded_card(draw, [440, 100, 840, 550], "#FFFFFF", "#F59E0B", width=2, radius=12)
    draw.text((460, 120), "Algorithmic Salience Function", font=heading_font, fill="#B45309")
    draw.text((460, 160), "Salience(S) = Freq(W) + alpha*Q + beta*Quant + gamma*Pos", font=sub_font, fill="#D97706")
    
    factors = [
        ("Term Frequency Weight", "Reward representative domain keywords"),
        ("Query Match Bonus (alpha = 2.5)", "High weight if sentence answers thematic query"),
        ("Quantitative Metric Bonus (beta = 2.0)", "Strong priority to empirical numbers (%, ms, x)"),
        ("Position Bias Weight (gamma = 1.0)", "Preference for initial topic-defining sentences")
    ]
    fy = 220
    for f_title, f_desc in factors:
        draw_rounded_card(draw, [455, fy, 825, fy + 65], "#FFFBEB", "#FDE68A", width=1, radius=6)
        draw.text((470, fy + 10), f_title, font=sub_font, fill="#92400E")
        draw.text((470, fy + 35), f_desc, font=small_font, fill="#78350F")
        fy += 75
        
    draw_arrow(draw, (845, 325), (925, 325), color="#10B981", width=3)
    
    # Box 3: Novelty Constraint & Synthesis
    draw_rounded_card(draw, [930, 100, 1250, 550], "#FFFFFF", "#10B981", width=2, radius=12)
    draw.text((950, 120), "Novelty Filter & Output", font=heading_font, fill="#065F46")
    draw.text((950, 155), "Jaccard Token Redundancy Gate:\nReject if Overlap(S_cand, S_sel) >= 4", font=small_font, fill="#047857")
    
    draw_rounded_card(draw, [945, 220, 1235, 370], "#ECFDF5", "#A7F3D0", width=1, radius=8)
    draw.text((960, 235), "Selected Slide Content:", font=sub_font, fill="#065F46")
    draw.text((960, 265), "* Bullet 1: Core paradigm\n* Bullet 2: Empirical 42% gain\n* Bullet 3: Broker design\n\nKey Takeaway: Autonomous\nlow-latency edge execution.", font=small_font, fill="#1E293B")
    
    draw_rounded_card(draw, [945, 390, 1235, 520], "#F0FDF4", "#86EFAC", width=1, radius=8)
    draw.text((960, 405), "Discourse Narration Script:", font=sub_font, fill="#166534")
    draw.text((960, 435), '"Moving onto system architecture,\nthe research introduces an edge\nbroker providing 42% speedup..."', font=small_font, fill="#14532D")
    
    img.save(os.path.join(out_dir, "fig4_textrank_salience.png"))
    print("Created fig4_textrank_salience.png")

# -------------------------------------------------------------
# Figure 5: High-Definition Slide Visual Layout
# -------------------------------------------------------------
def create_fig5():
    img = Image.new("RGB", (1300, 720), color="#0F172A")
    draw = ImageDraw.Draw(img)
    
    # Header area
    draw.rectangle([0, 0, 1300, 60], fill="#1E293B")
    draw.text((40, 18), "Figure 5: 1920x1080 High-Definition Presentation Slide Layout Architecture", font=title_font, fill="#F8FAFC")
    
    # Slide Container Simulation (16:9 ratio)
    sx, sy, sw, sh = 80, 90, 1140, 580
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill="#0A0F1D", outline="#3B82F6", width=2)
    
    # Slide Top Header
    draw.text((sx + 40, sy + 30), "DOCUVIDEO RAG EXPLAINER", font=small_font, fill="#60A5FA")
    draw.rounded_rectangle([sx + sw - 220, sy + 25, sx + sw - 40, sy + 60], radius=15, fill="#1E293B", outline="#3B82F6")
    draw.text((sx + sw - 200, sy + 33), "SLIDE 03 OF 05", font=sub_font, fill="#93C5FD")
    
    # Slide Title
    draw.text((sx + 40, sy + 75), "System Architecture & Pipeline Integration", font=title_font, fill="#FFFFFF")
    draw.line([sx + 40, sy + 120, sx + 500, sy + 120], fill="#3B82F6", width=3)
    
    # Card Container
    cx, cy, cw, ch = sx + 40, sy + 140, sw - 80, 340
    draw_rounded_card(draw, [cx, cy, cx + cw, cy + ch], "#111827", "#1F2937", width=2, radius=14)
    
    # Bullet Points
    bullets = [
        "Context-preserving sliding window chunking ensures semantic continuity across page breaks.",
        "Deterministic TextRank scoring selects quantitative findings and answers thematic queries.",
        "Thread-safe Windows SAPI5 offline synthesis generates crisp 22kHz speech narration."
    ]
    by = cy + 30
    for b in bullets:
        draw.ellipse([cx + 30, by + 5, cx + 46, by + 21], fill="#38BDF8")
        draw.text((cx + 65, by), b, font=sub_font, fill="#E2E8F0")
        by += 65
        
    # Takeaway Banner inside card
    draw.rounded_rectangle([cx + 25, cy + ch - 85, cx + cw - 25, cy + ch - 20], radius=10, fill="#1E293B", outline="#F59E0B")
    draw.text((cx + 45, cy + ch - 72), "KEY TAKEAWAY: Complete offline autonomy delivers enterprise-grade explanation with zero API costs.", font=sub_font, fill="#FCD34D")
    
    # Footer Metadata
    draw.text((sx + 40, sy + sh - 40), "Source Provenance: Pages 3, 5  |  Resolution: 1920x1080 Full HD  |  DocuVideo Offline Engine", font=small_font, fill="#64748B")
    
    img.save(os.path.join(out_dir, "fig5_slide_visual_hierarchy.png"))
    print("Created fig5_slide_visual_hierarchy.png")

# -------------------------------------------------------------
# Figure 6: DFD Level 0 Context Diagram
# -------------------------------------------------------------
def create_fig6():
    img = Image.new("RGB", (1200, 550), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1200, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 6: Data Flow Diagram (DFD Level 0 Context Diagram)", font=title_font, fill="#FFFFFF")
    
    # External Entity: User / Academic Researcher
    draw_rounded_card(draw, [60, 200, 300, 360], "#EFF6FF", "#2563EB", width=2, radius=12)
    draw.text((95, 230), "External Entity:", font=small_font, fill="#1E40AF")
    draw.text((95, 255), "User / Researcher", font=heading_font, fill="#1E3A8A")
    draw.text((95, 295), "(Uploads PDF, selects\nslide count & theme)", font=small_font, fill="#475569")
    
    # Arrow User -> System
    draw_arrow(draw, (305, 250), (475, 250), color="#2563EB", width=3)
    draw.text((320, 225), "PDF File + Params", font=small_font, fill="#1E40AF")
    
    # Arrow System -> User
    draw_arrow(draw, (475, 310), (305, 310), color="#059669", width=3)
    draw.text((315, 320), "MP4 Video + RAG Metrics", font=small_font, fill="#047857")
    
    # Central Process 0.0
    draw.ellipse([480, 150, 780, 420], fill="#FFFFFF", outline="#0F172A", width=3)
    draw.text((580, 210), "0.0", font=heading_font, fill="#0F172A")
    draw.text((515, 245), "DocuVideo RAG", font=title_font, fill="#1E293B")
    draw.text((510, 285), "Autonomous Explainer", font=heading_font, fill="#2563EB")
    draw.text((550, 320), "Engine System", font=sub_font, fill="#64748B")
    
    # Data Store 1: Local Vector Store
    draw.rectangle([920, 140, 1150, 230], fill="#F0FDF4", outline="#10B981", width=2)
    draw.line([920, 140, 920, 230], fill="#10B981", width=5)
    draw.line([1150, 140, 1150, 230], fill="#10B981", width=5)
    draw.text((940, 160), "D1: Local Vector Index", font=sub_font, fill="#065F46")
    draw.text((940, 190), "(ChromaDB / TF-IDF Chunks)", font=small_font, fill="#047857")
    
    # Arrows System <-> D1
    draw_arrow(draw, (770, 230), (915, 185), color="#10B981", width=2)
    draw_arrow(draw, (915, 205), (765, 260), color="#10B981", width=2)
    
    # Data Store 2: Local Cache & Media Output
    draw.rectangle([920, 330, 1150, 420], fill="#FAF5FF", outline="#A855F7", width=2)
    draw.line([920, 330, 920, 420], fill="#A855F7", width=5)
    draw.line([1150, 330, 1150, 420], fill="#A855F7", width=5)
    draw.text((940, 350), "D2: Output Media Storage", font=sub_font, fill="#6B21A8")
    draw.text((940, 380), "(WAV audio, PNGs, MP4)", font=small_font, fill="#581C87")
    
    # Arrow System -> D2
    draw_arrow(draw, (765, 330), (915, 375), color="#A855F7", width=2)
    
    img.save(os.path.join(out_dir, "fig6_dfd_level0.png"))
    print("Created fig6_dfd_level0.png")

# -------------------------------------------------------------
# Figure 7: DFD Level 1 Detailed Process Flow
# -------------------------------------------------------------
def create_fig7():
    img = Image.new("RGB", (1350, 700), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1350, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 7: Data Flow Diagram (DFD Level 1 Detailed Process Flow)", font=title_font, fill="#FFFFFF")
    
    # 6 Modular Processes
    processes = [
        ("1.0", "PDF Parsing & Clean", 60, 120),
        ("2.0", "Sliding Chunk Indexing", 480, 120),
        ("3.0", "Salience & Synthesis", 920, 120),
        ("4.0", "Visual Slide Render", 920, 440),
        ("5.0", "Voiceover Synthesis", 480, 440),
        ("6.0", "Video Multiplexing", 60, 440),
    ]
    
    for pid, pname, px, py in processes:
        draw_rounded_card(draw, [px, py, px + 350, py + 140], "#FFFFFF", "#334155", width=2, radius=12)
        draw.rounded_rectangle([px, py, px + 70, py + 50], radius=8, fill="#0F172A")
        draw.text((px + 18, py + 14), pid, font=sub_font, fill="#FFFFFF")
        draw.text((px + 85, py + 18), pname, font=heading_font, fill="#1E293B")
        
    # Detail descriptions inside processes
    draw.text((75, 185), "Input: PDF buffer\nOutput: Clean text & page map", font=small_font, fill="#475569")
    draw.text((495, 185), "Input: Normalized document\nOutput: Indexed vector chunks", font=small_font, fill="#475569")
    draw.text((935, 185), "Input: Thematic queries\nOutput: Structured slides & scripts", font=small_font, fill="#475569")
    draw.text((935, 505), "Input: Slide points & metadata\nOutput: 1920x1080 PNG images", font=small_font, fill="#475569")
    draw.text((495, 505), "Input: Spoken discourse scripts\nOutput: 22kHz WAV files + timing", font=small_font, fill="#475569")
    draw.text((75, 505), "Input: Slide PNGs + WAV audios\nOutput: Broadcast MP4 video", font=small_font, fill="#475569")
    
    # Connective Arrows
    # 1.0 -> 2.0
    draw_arrow(draw, (415, 190), (475, 190), color="#2563EB", width=3)
    # 2.0 -> 3.0
    draw_arrow(draw, (835, 190), (915, 190), color="#2563EB", width=3)
    # 3.0 -> 4.0
    draw_arrow(draw, (1100, 265), (1100, 435), color="#A855F7", width=3)
    # 3.0 -> 5.0 (diagonal)
    draw_arrow(draw, (930, 265), (750, 435), color="#F97316", width=3)
    # 4.0 -> 6.0
    draw_arrow(draw, (915, 530), (835, 530), color="#10B981", width=3)
    # 5.0 -> 6.0
    draw_arrow(draw, (475, 510), (415, 510), color="#10B981", width=3)
    
    img.save(os.path.join(out_dir, "fig7_dfd_level1.png"))
    print("Created fig7_dfd_level1.png")

# -------------------------------------------------------------
# Figure 8: Audio-Visual Synchronization Timeline Model
# -------------------------------------------------------------
def create_fig8():
    img = Image.new("RGB", (1300, 580), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1300, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 8: Audio-Visual Synchronization and Timeline Assembly Model", font=title_font, fill="#FFFFFF")
    
    # Time Axis
    draw.line([80, 480, 1220, 480], fill="#334155", width=3)
    for tx in range(100, 1220, 200):
        draw.line([tx, 475, tx, 485], fill="#334155", width=2)
        sec = (tx - 100) // 10
        draw.text((tx - 15, 495), f"t = {sec}s", font=small_font, fill="#475569")
    draw.text((1230, 472), "Time (s)", font=sub_font, fill="#0F172A")
    
    # Slide Track 1 & Audio Track 1
    draw.text((80, 95), "Track 1: Visual Slides (1080p)", font=heading_font, fill="#1E40AF")
    draw_rounded_card(draw, [100, 130, 420, 230], "#DBEAFE", "#2563EB", width=2, radius=8)
    draw.text((120, 150), "Slide 01 Clip (Intro)", font=sub_font, fill="#1E40AF")
    draw.text((120, 185), "Duration = T_audio1 + 0.4s", font=small_font, fill="#334155")
    
    # Slide Track 2
    draw_rounded_card(draw, [400, 130, 780, 230], "#DBEAFE", "#2563EB", width=2, radius=8)
    draw.text((430, 150), "Slide 02 Clip (Architecture)", font=sub_font, fill="#1E40AF")
    draw.text((430, 185), "Duration = T_audio2 + 0.4s", font=small_font, fill="#334155")
    
    # Crossfade indicator 1
    draw.rectangle([400, 130, 420, 230], fill="#FDE047", outline="#CA8A04")
    draw.text((375, 80), "Crossfade (0.5s)", font=small_font, fill="#854D0E")
    draw_arrow(draw, (410, 100), (410, 125), color="#CA8A04", width=2)
    
    # Slide Track 3
    draw_rounded_card(draw, [760, 130, 1180, 230], "#DBEAFE", "#2563EB", width=2, radius=8)
    draw.text((790, 150), "Slide 03 Clip (Results & Conclusion)", font=sub_font, fill="#1E40AF")
    draw.text((790, 185), "Duration = T_audio3 + 0.4s", font=small_font, fill="#334155")
    
    # Crossfade indicator 2
    draw.rectangle([760, 130, 780, 230], fill="#FDE047", outline="#CA8A04")
    
    # Track 2: Audio Narration
    draw.text((80, 275), "Track 2: Voiceover Speech Narration (22kHz SAPI5 WAV)", font=heading_font, fill="#15803D")
    
    draw_rounded_card(draw, [100, 310, 410, 390], "#DCFCE7", "#16A34A", width=2, radius=8)
    draw.text((120, 330), "Narration Track 1", font=sub_font, fill="#15803D")
    draw.text((120, 355), "Measured WAV Length: 24.2s", font=small_font, fill="#14532D")
    
    draw_rounded_card(draw, [420, 310, 770, 390], "#DCFCE7", "#16A34A", width=2, radius=8)
    draw.text((440, 330), "Narration Track 2", font=sub_font, fill="#15803D")
    draw.text((440, 355), "Measured WAV Length: 31.8s", font=small_font, fill="#14532D")
    
    draw_rounded_card(draw, [780, 310, 1170, 390], "#DCFCE7", "#16A34A", width=2, radius=8)
    draw.text((800, 330), "Narration Track 3", font=sub_font, fill="#15803D")
    draw.text((800, 355), "Measured WAV Length: 34.5s", font=small_font, fill="#14532D")
    
    # Dynamic sync annotation
    draw.text((80, 430), "Dynamic Invariant: For every slide i, Video Duration D_i = Audio Duration A_i + delta, ensuring zero premature slide advances.", font=body_font, fill="#1E293B")
    
    img.save(os.path.join(out_dir, "fig8_audio_video_timeline.png"))
    print("Created fig8_audio_video_timeline.png")

# -------------------------------------------------------------
# Figure 9: Execution Performance Breakdown
# -------------------------------------------------------------
def create_fig9():
    img = Image.new("RGB", (1200, 580), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw.rectangle([0, 0, 1200, 55], fill="#0F172A")
    draw.text((30, 14), "Figure 9: Latency Breakdown Across Pipeline Execution Stages", font=title_font, fill="#FFFFFF")
    
    data = [
        ("PDF Ingestion & Text Cleanup", 0.45, "#3B82F6"),
        ("ChromaDB / TF-IDF Vector Indexing", 1.93, "#10B981"),
        ("Thematic Query Retrieval & Salience", 0.38, "#A855F7"),
        ("Pillow 1080p Slide Graphics Render", 0.56, "#F97316"),
        ("Windows SAPI5 Voiceover Synthesis", 0.73, "#06B6D4"),
        ("MoviePy Multi-Track Video Encoding", 114.40, "#EC4899"),
    ]
    
    max_val = 120.0
    chart_x = 360
    chart_y = 100
    chart_w = 750
    bar_h = 45
    gap = 25
    
    for i, (label, val, color) in enumerate(data):
        y = chart_y + i * (bar_h + gap)
        # Label
        draw.text((40, y + 12), label, font=sub_font, fill="#1E293B")
        
        # Bar
        b_len = int((val / max_val) * chart_w)
        if b_len < 10:
            b_len = 10
        draw_rounded_card(draw, [chart_x, y, chart_x + b_len, y + bar_h], color, color, width=1, radius=6)
        
        # Text on or near bar
        t_str = f"{val:.2f}s"
        if b_len > 80:
            draw.text((chart_x + b_len - 70, y + 12), t_str, font=sub_font, fill="#FFFFFF")
        else:
            draw.text((chart_x + b_len + 15, y + 12), t_str, font=sub_font, fill="#0F172A")
            
    # X-axis scale
    axis_y = chart_y + len(data) * (bar_h + gap) + 10
    draw.line([chart_x, axis_y, chart_x + chart_w, axis_y], fill="#64748B", width=2)
    for s_val in [0, 20, 40, 60, 80, 100, 120]:
        sx = chart_x + int((s_val / max_val) * chart_w)
        draw.line([sx, axis_y, sx, axis_y + 8], fill="#64748B", width=2)
        draw.text((sx - 10, axis_y + 14), f"{s_val}s", font=small_font, fill="#475569")
    draw.text((chart_x + chart_w // 2 - 40, axis_y + 40), "Execution Latency (Seconds)", font=sub_font, fill="#0F172A")
    
    img.save(os.path.join(out_dir, "fig9_execution_performance_chart.png"))
    print("Created fig9_execution_performance_chart.png")

if __name__ == "__main__":
    create_fig1()
    create_fig2()
    create_fig3()
    create_fig4()
    create_fig5()
    create_fig6()
    create_fig7()
    create_fig8()
    create_fig9()
    print("All 9 figures generated successfully!")
