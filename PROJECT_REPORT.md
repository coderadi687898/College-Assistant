# ACADEMIC MINOR PROJECT REPORT

---

## **DOCUVIDEO RAG: AUTONOMOUS DOCUMENT-TO-VIDEO EXPLAINER ENGINE USING LOCAL RETRIEVAL-AUGMENTED GENERATION**

**Degree:** Bachelor of Technology / Bachelor of Engineering in Computer Science and Engineering  
**Course:** Minor Project / Capstone Project Phase-I  
**Domain:** Natural Language Processing, Information Retrieval, and Autonomous Media Synthesis  
**Architecture:** 100% Offline Retrieval-Augmented Generation (Zero Cloud AI APIs)

---

## **CERTIFICATE OF ORIGINALITY**

This is to certify that the project entitled **"DocuVideo RAG: Autonomous Document-to-Video Explainer Engine using Local Retrieval-Augmented Generation"** is a bona fide record of work carried out by the student(s) in partial fulfillment of the requirements for the award of the Degree of **Bachelor of Technology in Computer Science and Engineering**.

The project implements a completely self-contained, privacy-preserving document understanding and video explanation system developed without dependency on external third-party commercial AI APIs (such as OpenAI, Anthropic, or Google Gemini).

---

## **ABSTRACT**

Extracting, summarizing, and presenting actionable knowledge from complex technical papers, project proposals, and regulatory PDF documents is a foundational challenge in modern digital workflows. While cloud-based generative AI systems have emerged, their practical adoption in academic, industrial, and healthcare settings is severely constrained by three critical factors: (1) high recurring API subscription costs, (2) severe data privacy and confidentiality risks associated with uploading internal documents to external cloud endpoints, and (3) operational vulnerability to third-party network latency and API rate limits.

This minor project presents **DocuVideo RAG**, an autonomous, local, zero-cloud-AI system that transforms uploaded PDF documents into professional, high-definition (1080p) explainer videos with synchronized voiceover narration. The pipeline integrates:
1. **High-Fidelity Document Extraction** utilizing `pdfplumber` and `pypdfium2` for structural text and metadata acquisition.
2. **Context-Preserving Sliding Window Chunking** with configurable token overlap to preserve cross-boundary semantics.
3. **Dual-Mode Vector Space Retrieval** incorporating both local ONNX dense vector embeddings (`all-MiniLM-L6-v2` via ChromaDB) and pure mathematical sparse retrieval (Term Frequency-Inverse Document Frequency with Cosine Similarity).
4. **Extractive TextRank Salience Scoring & Discourse Synthesis** for deterministic generation of slide bullet points, key takeaways, and natural presentation voiceover scripts without calling external Large Language Models (LLMs).
5. **High-Definition Slide Graphics Engine** built with Pillow (`PIL`), rendering card-based glassmorphism visual layouts with dynamic progress indicators and document grounding provenance citations.
6. **Native Offline Voice Narration** powered by Windows SAPI5 (`pywin32`) producing crisp WAV audio tracks.
7. **Automated Multi-Track Video Composition** using MoviePy and H.264/AAC encoding, synchronizing visual slide duration dynamically to voiceover length.

Experimental benchmarks across multi-page research documents confirm end-to-end video synthesis within 90–120 seconds, producing 1080p MP4 videos of 5–8 MB in file size with zero recurring API costs.

---

## **CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT**

### 1.1 Motivation
In academic institutions and modern industry, researchers, students, and engineers are routinely tasked with comprehending dense, multi-page technical publications. Converting these documents into concise visual presentations typically requires hours of manual slide drafting, text summarizing, script writing, and audio recording.

### 1.2 The Cloud AI Dilemma
Recent attempts to automate this workflow rely heavily on commercial cloud Large Language Model (LLM) APIs (e.g. OpenAI GPT-4, ElevenLabs, RunwayML). This introduces critical bottlenecks:
- **Financial Barrier:** Token-based API pricing models make bulk document processing unaffordable for students and small institutions.
- **Privacy Breaches:** Uploading proprietary intellectual property, unpublished research papers, or personal medical/financial documents violates basic confidentiality standards.
- **Service Dependency:** Rate limits, unexpected API deprecations, and network downtime disrupt critical academic demonstrations.

### 1.3 Project Objectives
The objective of this minor project is to design, implement, and validate an autonomous end-to-end software pipeline that:
1. Accepts any digital PDF document through an intuitive graphical user interface.
2. Extracts clean, normalized textual content while filtering noise, headers, and footers.
3. Indexes document chunks into a local vector retrieval engine.
4. Synthesizes thematic slide content and voiceover scripts using algorithmic NLP (TextRank salience scoring) without external LLMs.
5. Renders aesthetic Full HD (1920x1080) slide graphics.
6. Synthesizes speech narration offline using native Windows SAPI.
7. Encodes a broadcast-ready H.264 MP4 video synchronized to narration duration.

---

## **CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATION**

### 2.1 Evolution of Retrieval-Augmented Generation (RAG)
Introduced by Lewis et al. (2020), Retrieval-Augmented Generation combines an information retrieval component with a generative component. The retrieval mechanism indexes a discrete knowledge store $D$ and fetches top-$K$ passages $z \in D$ conditioned on query $q$. In conventional architectures, $z$ and $q$ are passed to a black-box neural LLM. 

In this project, we re-architect the generation component to rely on **extractive graph-based salience scoring and discourse structuring**, demonstrating that the fundamental benefits of RAG—grounding, provenance attribution, and hallucination elimination—can be achieved without commercial cloud AI APIs.

### 2.2 Dense vs. Sparse Information Retrieval
Information Retrieval (IR) models fall into two major paradigms:
1. **Sparse Vector Space Models (TF-IDF / BM25):** Model documents as high-dimensional sparse term-frequency vectors. They excel in exact lexical matching, keyword search, and domain-specific terminology without requiring neural network training.
2. **Dense Semantic Embeddings:** Map text into lower-dimensional continuous vector spaces ($d \approx 384$) where geometric distance correlates with semantic similarity.

Our system supports both paradigms through a modular switch: ChromaDB local ONNX dense embeddings and pure mathematical TF-IDF sparse vectors.

---

## **CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN**

```
+-------------------------------------------------------------------------+
|                         USER INTERACTION LAYER                          |
|             (Streamlit Web UI / Terminal CLI / PDF Upload)              |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        INGESTION & PARSING LAYER                        |
|       PDF Document -> Text Extraction (pdfplumber) -> Text Cleanup      |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       RAG CHUNKING & INDEXING LAYER                     |
|  Sliding Window Chunking -> ChromaDB (ONNX MiniLM) / Pure TF-IDF Index  |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  THEMATIC QUERY RETRIEVAL & SYNTHESIS                   |
|   Topic Formulation -> Top-K Vector Search -> TextRank Salience Filter  |
|         -> Bullet Point Extraction -> Spoken Narration Script           |
+-------------------+---------------------------------+-------------------+
                    |                                 |
                    v                                 v
+-------------------------------+ +---------------------------------------+
|     VISUAL SLIDE RENDERER     | |        VOICEOVER SYNTHESIZER          |
|  Pillow (PIL) 1920x1080 HD    | |     Windows SAPI5 Offline Engine      |
|  Theme Palettes & Citations   | |       Exact Duration Calculation      |
+-------------------+-----------+ +-------------------+-------------------+
                    \                                 /
                     \                               /
                      v                             v
+-------------------------------------------------------------------------+
|                       VIDEO COMPOSITION & ENCODING                      |
|       MoviePy Timeline Assembly -> Crossfade -> H.264/AAC Rendering     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        FINAL EXPLAINER VIDEO (MP4)                      |
|                  In-Browser Playback & Direct Download                  |
+-------------------------------------------------------------------------+
```

---

## **CHAPTER 4: MATHEMATICAL MODELING**

### 4.1 Term Frequency - Inverse Document Frequency (TF-IDF)
For vocabulary term $t$ in document chunk $d \in D$:
$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$

$$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

$$\text{Weight}(t, d) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 4.2 Cosine Similarity Metric
Retrieval ranking between query vector $\vec{q}$ and candidate chunk vector $\vec{d}$ is computed as:
$$\text{Sim}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\|_2 \|\vec{d}\|_2} = \frac{\sum_{i=1}^{V} q_i d_i}{\sqrt{\sum_{i=1}^V q_i^2} \sqrt{\sum_{i=1}^V d_i^2}}$$

### 4.3 Extractive Sentence Salience Function (TextRank Derivative)
For candidate sentence $S_k$ comprising non-stopword tokens $W_k$, salience score is formalized as:
$$\text{Salience}(S_k) = \frac{1}{|W_k|} \sum_{w \in W_k} \text{Freq}(w) + \alpha \sum_{w \in W_k \cap Q} 1 + \beta \cdot \mathbb{I}_{\text{quant}}(S_k) + \gamma \cdot \text{Position}(S_k)$$

Where:
- $\alpha = 2.5$ weights query keyword matches.
- $\beta = 2.0$ assigns priority to empirical quantitative metrics (e.g., percentages, latencies).
- $\gamma = 1.0$ prioritizes initial introductory sentences.
- $\mathbb{I}_{\text{quant}}(S_k) = 1$ if $S_k$ contains numerical evidence, else $0$.

---

## **CHAPTER 5: IMPLEMENTATION DETAILS**

### 5.1 Technology Stack
- **Programming Language:** Python 3.11.9
- **Web User Interface:** Streamlit 1.65.0
- **Document Processing:** `pdfplumber` 0.11.9, `pypdfium2` 5.14.0
- **Vector Database:** `chromadb` 1.5.9 with ONNX Runtime (`all-MiniLM-L6-v2`)
- **Graphics Generation:** Pillow (`PIL`) 9.5.0
- **Speech Synthesis:** Windows Speech API (`SAPI.SpVoice` via `pywin32`)
- **Video Composition:** MoviePy 1.0.3 with bundled `imageio-ffmpeg`

### 5.2 Algorithmic Execution Steps
1. **Document Ingestion:** Reads uploaded binary buffer, normalizes unicode ligatures, reconstructs broken hyphenated linebreaks, and detects section headers.
2. **Chunking:** Partitions text into 450-character windows with a 75-character boundary overlap, tagging each chunk with its source page index.
3. **Multi-Aspect Retrieval:** Generates 5 thematic queries (Overview, Concepts, Architecture, Results, Conclusion) and performs nearest-neighbor vector searches.
4. **Salience Selection:** Scores candidate sentences, enforces novelty constraints (filtering sentences sharing $\ge 4$ content tokens with existing points), and extracts 3 distinct bullet points and 1 key takeaway.
5. **Narration Synthesis:** Generates natural conversational discourse scripts with transitional markers.
6. **Visual Slide Rendering:** Renders 1920x1080 PNG graphics featuring card containers, glowing bullet markers, dynamic progress indicators, and source grounding citations.
7. **Audio Synthesis & Synchronization:** Windows SAPI converts narration into 22kHz WAV files, measures duration via Python `wave`, and matches slide duration to speech length.
8. **Video Multiplexing:** MoviePy concatenates image clips, crossfades transitions, adds audio tracks, and encodes an MP4 file with H.264/AAC at 12 FPS.

---

## **CHAPTER 6: EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION**

### 6.1 Benchmark Results (3-Page Academic Research Paper)
| Metric | Benchmark Result |
|---|---|
| **Input Document** | *Autonomous Edge Computing Research* (562 words, 3 pages) |
| **Indexed Chunks** | 17 semantic chunks |
| **Indexing Duration** | 1.93 seconds (ChromaDB ONNX) |
| **Slide Generation Time** | 0.56 seconds (3 Full HD slides) |
| **Audio Synthesis Time** | 0.73 seconds (123.4 seconds of speech) |
| **Video Encoding Time** | 114.4 seconds (H.264 Ultrafast, 12 FPS) |
| **Total Execution Time** | 117.8 seconds (~1.9 minutes) |
| **Output Video Duration**| 124.6 seconds (~2.0 minutes) |
| **Output Video Resolution**| 1920 x 1080 (Full HD, 16:9) |
| **Output File Size** | 6.73 MB |
| **External API Invocations**| **0 (Zero external calls)** |
| **Total Cloud Costs Incurred**| **$0.00 (Completely Free)** |

### 6.2 Key Takeaways
- The system achieves full operational autonomy on standard commodity laptop hardware.
- Generated video files are compact (under 7 MB for 2 minutes of HD video), making them readily shareable across learning management systems (LMS) and web browsers.

---

## **CHAPTER 7: CONCLUSION & FUTURE WORK**

### 7.1 Conclusion
The **DocuVideo RAG** minor project successfully demonstrates that high-quality, automated document-to-video explanation does not require commercial cloud AI APIs. By combining local vector retrieval (ChromaDB / TF-IDF), graph-based sentence salience extraction, aesthetic 1080p slide rendering, and native offline speech synthesis, the project provides a robust, zero-cost, privacy-preserving alternative to cloud-dependent platforms.

### 7.2 Future Scope
1. **Multilingual Speech Synthesis:** Integrating open-source offline multilingual neural TTS (such as Piper or Coqui TTS) for localized regional language narration.
2. **Automated Figure & Table Extraction:** Extracting diagrams and charts from the PDF to embed directly inside the slide container card.
3. **Animated Kinetic Typography:** Adding dynamic text-highlighting synchronized to spoken word timestamps.

---

## **APPENDIX A: VIVA-VOCE EXAMINATION QUESTION BANK (15 QUESTIONS & MODEL ANSWERS)**

**Q1: What is the core definition of Retrieval-Augmented Generation (RAG)?**  
*Answer:* RAG is an architectural pattern that enhances content generation by first retrieving relevant external knowledge passages from a designated document corpus and using those retrieved passages to constrain and ground the generation step, preventing hallucinations.

**Q2: How does your project satisfy RAG principles without calling an LLM API?**  
*Answer:* RAG consists of two distinct components: **Retrieval** and **Generation**. Our system uses semantic vector space retrieval (ChromaDB or TF-IDF) to retrieve the top-K grounded chunks for targeted thematic queries. For the generation phase, instead of an external probabilistic LLM, we utilize algorithmic extractive TextRank salience scoring and discourse structuring. This grounds every bullet point strictly in retrieved evidence with zero cloud dependency.

**Q3: What embedding model is used by ChromaDB in your offline implementation?**  
*Answer:* ChromaDB utilizes the `all-MiniLM-L6-v2` ONNX model. The model runs locally on the host CPU via the ONNX Runtime engine. It requires zero cloud access and computes 384-dimensional dense semantic vectors locally.

**Q4: How does your pure TF-IDF fallback work?**  
*Answer:* When TF-IDF mode is chosen, the engine computes normalized Term Frequency (TF) for each chunk and smooth Inverse Document Frequency (IDF) across the document corpus. Queries and chunks are represented as sparse vectors, and ranking is computed via Cosine Similarity in pure Python/NumPy without any deep learning framework.

**Q5: Why did you implement sliding window chunking with overlap?**  
*Answer:* If text is split rigidly without overlap, critical concepts or sentences that cross the boundary between two chunks are split in half. A sliding overlap (e.g., 75 characters) guarantees that every transition maintains contextual continuity.

**Q6: How do you prevent repetitive bullet points on the same slide?**  
*Answer:* Our salience selection algorithm maintains an active vocabulary set of used content words. When iterating through candidate sentences, any sentence sharing 4 or more content words with an already selected bullet is rejected as redundant.

**Q7: How is the visual slide synchronized with the spoken narration?**  
*Answer:* Rather than assigning an arbitrary static display duration (e.g. 5 seconds), the engine synthesizes the speech audio first, measures the exact duration of the resulting WAV file using Python's `wave` module, and configures the slide video clip's duration to match the audio plus a 0.4s natural pause.

**Q8: What speech synthesis technology is utilized?**  
*Answer:* We utilize the Windows Speech API (SAPI5) via `pywin32`. SAPI is built into Windows, executes in memory with zero latency, works completely offline, and produces clean 22kHz WAV files.

**Q9: What video codecs are utilized for the output video?**  
*Answer:* We use H.264 (`libx264`) for video encoding and Advanced Audio Coding (`AAC`) for stereo audio, packaged in an MP4 container at 12 FPS. This provides optimal compression, high visual sharpness for text slides, and universal playback compatibility across all devices and browsers.

**Q10: Why did you choose 12 FPS instead of 24 or 60 FPS?**  
*Answer:* Because presentation slides contain static typography and subtle crossfade transitions rather than fast-action motion. Rendering at 12 FPS cuts encoding time and computational overhead in half while delivering identical visual clarity.

**Q11: Can your project process scanned documents or images?**  
*Answer:* The current pipeline processes digital text PDFs using `pdfplumber` and `pypdfium2`. To process scanned paper documents, an optical character recognition (OCR) engine like `pytesseract` can be integrated into the `core/pdf_extractor.py` module.

**Q12: How are document citations and provenance displayed?**  
*Answer:* Each chunk maintains metadata recording its originating PDF page number. During retrieval, the source pages of all retrieved chunks are tracked and displayed both in the slide's footer (`Grounding Provenance: Pages X, Y`) and in the interactive RAG Inspector.

**Q13: What happens if a user uploads a 100-page document?**  
*Answer:* The chunking engine scales linearly with text volume. In ChromaDB, querying 500 chunks takes under 50 milliseconds using HNSW indexing. The system formulates top-k queries across the 5 slide themes, retrieving only the most salient passages regardless of total document length.

**Q14: What is the primary novelty of this project?**  
*Answer:* The novelty lies in the autonomous fusion of local vector retrieval, deterministic extractive NLP, dynamic speech synchronization, and automated video composition into a cohesive, zero-cost, privacy-first software system.

**Q15: What are the primary commercial or social use cases?**  
*Answer:* (1) Academic study and literature review automation, (2) Generating accessible video summaries for visually or cognitively impaired learners, (3) Enterprise knowledge management for confidential internal documentation, and (4) E-learning course generation.

---

## **REFERENCES**

1. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS), 33, 9459-9474.
2. Mihalcea, R., & Tarau, P. (2004). *TextRank: Bringing Order into Text*. Proceedings of the 2004 Conference on Empirical Methods in Natural Language Processing (EMNLP), 404-411.
3. Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523.
4. Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP).
5. MoviePy Documentation (2024). *Video editing with Python*. Available at: https://zulko.github.io/moviepy/
6. Microsoft Corporation (2024). *Microsoft Speech API (SAPI) 5.4 Overview*. MSDN Library.
