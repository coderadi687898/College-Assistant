"""
Local Retrieval-Augmented Generation (RAG) Engine
Indexes document chunks into local vector space and synthesizes structured
presentation slides and natural narration scripts without external AI APIs.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import numpy as np
import chromadb

from .pdf_extractor import PDFExtractionResult


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    page_number: int


@dataclass
class SlideContent:
    slide_index: int
    category: str
    title: str
    bullet_points: List[str]
    key_takeaway: str
    narration_script: str
    source_pages: List[int]


STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "his", "how", "if", "in", "into",
    "is", "it", "its", "more", "most", "my", "no", "nor", "not", "of", "off", "on", "once", "only",
    "or", "other", "our", "out", "over", "own", "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your"
}


def tokenize(text: str) -> List[str]:
    return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_\-]{2,}\b', text)]


class LocalRAGEngine:
    """
    RAG Engine for offline document analysis and slide/script synthesis.
    """

    def __init__(self, extraction: PDFExtractionResult, chunk_size: int = 450, chunk_overlap: int = 75):
        self.extraction = extraction
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunks = self._create_chunks()
        self.collection = self._init_chroma()

    def _create_chunks(self) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        counter = 1

        for page in self.extraction.pages:
            text = page.text.strip()
            if not text:
                continue

            raw_sentences = re.split(r'(?<=[.!?])\s+|\n\n+', text)
            sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 15]

            current = []
            curr_len = 0
            for sent in sentences:
                s_len = len(sent)
                if curr_len + s_len > self.chunk_size and current:
                    chunk_text = " ".join(current)
                    chunks.append(DocumentChunk(
                        chunk_id=f"c_{page.page_number}_{counter}",
                        text=chunk_text,
                        page_number=page.page_number
                    ))
                    counter += 1
                    overlap_sent = [current[-1]] if self.chunk_overlap > 0 else []
                    current = overlap_sent + [sent]
                    curr_len = sum(len(s) for s in current)
                else:
                    current.append(sent)
                    curr_len += s_len

            if current:
                chunk_text = " ".join(current)
                chunks.append(DocumentChunk(
                    chunk_id=f"c_{page.page_number}_{counter}",
                    text=chunk_text,
                    page_number=page.page_number
                ))
                counter += 1

        return chunks

    def _init_chroma(self):
        """Initializes local in-memory ChromaDB vector store."""
        import uuid
        client = chromadb.Client()
        col = client.create_collection(
            name=f"rag_{uuid.uuid4().hex[:8]}",
            metadata={"hnsw:space": "cosine"}
        )
        if self.chunks:
            col.add(
                documents=[c.text for c in self.chunks],
                ids=[c.chunk_id for c in self.chunks],
                metadatas=[{"page": c.page_number} for c in self.chunks]
            )
        return col

    def retrieve(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """Retrieves top-k relevant chunks for a topic query."""
        if not self.chunks:
            return []
        k = min(top_k, len(self.chunks))
        res = self.collection.query(query_texts=[query], n_results=k)

        results = []
        chunk_map = {c.chunk_id: c for c in self.chunks}
        if res and res.get("ids") and res["ids"][0]:
            for cid in res["ids"][0]:
                if cid in chunk_map:
                    results.append(chunk_map[cid])
        return results if results else self.chunks[:k]

    def _extract_salient_points(self, retrieved: List[DocumentChunk], keywords: List[str]) -> Tuple[List[str], str]:
        """Extracts top non-redundant key sentences using term salience and keyword relevance."""
        candidates = []
        for c in retrieved:
            for s in re.split(r'(?<=[.!?])\s+', c.text):
                cleaned = s.strip().rstrip('. ')
                if 25 <= len(cleaned) <= 160:
                    candidates.append(cleaned)

        if not candidates:
            return (["Key information extracted from document."], "Core finding from the material.")

        words = [w for sent in candidates for w in tokenize(sent) if w not in STOPWORDS]
        word_freq = Counter(words)

        scored = []
        for idx, sent in enumerate(candidates):
            tokens = [w for w in tokenize(sent) if w not in STOPWORDS]
            if not tokens:
                continue
            freq_score = sum(word_freq[t] for t in tokens) / len(tokens)
            topic_bonus = sum(2.5 for t in tokens if t in keywords)
            num_bonus = 2.0 if re.search(r'\b\d+(\.\d+)?%?|\b\d+\b', sent) else 0.0
            pos_bonus = 1.0 if idx < 3 else 0.0
            scored.append((freq_score + topic_bonus + num_bonus + pos_bonus, sent))

        scored.sort(key=lambda x: x[0], reverse=True)

        selected = []
        used_words = set()
        for score, sent in scored:
            tokens = set(tokenize(sent)) - STOPWORDS
            if len(tokens & used_words) < 4:
                selected.append(sent)
                used_words.update(tokens)
            if len(selected) >= 3:
                break

        if not selected and scored:
            selected = [s[1] for s in scored[:3]]

        takeaway = selected[0] if selected else "Key strategic takeaway."
        for _, sent in scored:
            if re.search(r'\b(result|demonstrate|show|reduce|achieve|increase|conclude)\b', sent, re.I):
                takeaway = sent
                break

        return selected, takeaway

    def _synthesize_script(self, category: str, title: str, bullets: List[str], takeaway: str, idx: int, total: int) -> str:
        """Composes clean conversational voiceover narration for the slide."""
        if idx == 1:
            intro = f"Welcome to this presentation on {title}."
        elif idx == total:
            intro = f"Finally, let us review our conclusion on {title.lower()}."
        else:
            transitions = ["In this section, we examine", "Next, turning to our analysis of", "Continuing with"]
            intro = f"{transitions[(idx - 2) % len(transitions)]} {title.lower()}."

        points_text = " ".join([f"Key point: {b.rstrip('.')}." for b in bullets])
        conclusion_text = f"In summary: {takeaway.rstrip('.')}."
        return f"{intro} {points_text} {conclusion_text}"

    def generate_slides(self, num_slides: int = 4) -> List[SlideContent]:
        """Generates slide deck content from retrieved chunks."""
        num_slides = max(3, min(6, num_slides))
        doc_title = self.extraction.metadata.title

        topics = [
            ("EXECUTIVE SUMMARY", "Overview & Motivation", "overview abstract introduction motivation background problem goal", ["overview", "introduction", "background", "motivation"]),
            ("SYSTEM ARCHITECTURE", "Architecture & Core Concepts", "architecture system design components layer framework modules", ["architecture", "system", "design", "component", "layer"]),
            ("METHODOLOGY", "Methodology & Execution", "methodology protocol algorithm workflow execution technique process", ["methodology", "algorithm", "workflow", "process"]),
            ("RESULTS & EVALUATION", "Key Findings & Results", "results evaluation benchmarks performance metrics reduction test", ["results", "evaluation", "performance", "metrics"]),
            ("CONCLUSION", "Conclusion & Future Scope", "conclusion summary future work outlook recommendations takeaways", ["conclusion", "summary", "future", "outlook"])
        ]

        if num_slides == 3:
            selected_topics = [topics[0], topics[1], topics[3]]
        elif num_slides == 4:
            selected_topics = [topics[0], topics[1], topics[3], topics[4]]
        elif num_slides == 5:
            selected_topics = topics
        else:
            selected_topics = topics + [("KEY TAKEAWAYS", "Strategic Highlights", "advantages benefits impact analysis takeaways", ["advantages", "benefits", "impact"])]

        slides: List[SlideContent] = []
        for i, (cat, default_title, query, kw) in enumerate(selected_topics, start=1):
            retrieved = self.retrieve(query, top_k=3)
            pages = sorted(list(set(c.page_number for c in retrieved))) or [1]
            title = doc_title if (i == 1 and len(doc_title) < 55) else default_title
            bullets, takeaway = self._extract_salient_points(retrieved, kw)
            script = self._synthesize_script(cat, title, bullets, takeaway, i, len(selected_topics))

            slides.append(SlideContent(
                slide_index=i,
                category=cat,
                title=title,
                bullet_points=bullets,
                key_takeaway=takeaway,
                narration_script=script,
                source_pages=pages
            ))

        return slides
