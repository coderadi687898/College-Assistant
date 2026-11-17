# Academic Minor Project Report Content for DocuVideo RAG
# Department of Computer Science and Engineering, IIIT Bhopal

SECTIONS_DATA = {
    "project_title": "DOCUVIDEO RAG: AUTONOMOUS DOCUMENT-TO-VIDEO EXPLAINER ENGINE USING LOCAL RETRIEVAL-AUGMENTED GENERATION",
    "phase": "PROJECT REPORT [Phase-I]",
    "degree": "BACHELOR OF TECHNOLOGY",
    "department": "Department of Computer Science and Engineering",
    "institute": "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY BHOPAL (M.P.)",
    "student1": "Aditya (Scholar No.: 2111100XX, VII Semester)",
    "student2": "Co-Author Name (Scholar No.: 2111100YY, VII Semester)",
    "supervisor": "Dr. Supervisor Name",
    "designation": "Assistant Professor / Associate Professor",
    "academic_year": "2025–2026",
    "month_year": "October 2026",
}

ACKNOWLEDGEMENT_TEXT = """We, Aditya and Co-Author, would like to express our deepest gratitude and sincere appreciation to everyone who supported, inspired, and guided us throughout the conceptualization, system architecture design, and successful realization of our minor project titled "DocuVideo RAG: Autonomous Document-to-Video Explainer Engine using Local Retrieval-Augmented Generation".

First and foremost, we express our profound gratitude to our esteemed Director, Indian Institute of Information Technology, Bhopal, for creating an inspiring academic and research ecosystem and providing state-of-the-art computational infrastructure and facilities that enabled us to pursue and successfully execute this research project.

We express our heartfelt appreciation and profound indebtedness to our Project Guide, Dr. Supervisor Name, Department of Computer Science and Engineering, for his invaluable guidance, technical mentorship, insightful critiques, and unwavering encouragement throughout every phase of our work. His meticulous review of our system design, algorithmic formulations, and experimental evaluations played an indispensable role in shaping the technical rigor and quality of this project.

We extend our sincere thanks to the Department Coordinator and Head of Department, Department of Computer Science and Engineering, IIIT Bhopal, for administrative support, curriculum guidance, and facilitating timely project evaluations. We also express our sincere gratitude to all the respected faculty members and technical staff of the Department of Computer Science and Engineering for sharing their profound academic knowledge, clarifying intricate theoretical queries, and fostering an environment of innovation.

We are deeply grateful to our batchmates, peers, and friends whose active discussions, constructive feedback during user evaluations, and constant encouragement provided intellectual vitality during challenging development phases.

Finally, we convey our deepest love and emotional gratitude to our parents and family members. Their unconditional sacrifices, enduring patience, continuous prayers, and moral support have been our foundational pillars of strength and motivation throughout our academic journey. We dedicate the success of this project to their unwavering faith in our potential."""

AREA_OF_WORK_TEXT = """The primary research domain of this minor project encompasses Natural Language Processing (NLP), Information Retrieval (IR), and Automated Multimedia Synthesis, with specialized focus on Local Privacy-Preserving Retrieval-Augmented Generation (Local RAG) and Edge Media Composition.

While contemporary artificial intelligence paradigms have increasingly transitioned toward cloud-hosted Large Language Model (LLM) APIs, this project addresses the critical technological and privacy bottlenecks associated with cloud dependencies. In enterprise, defense, healthcare, and academic sectors, confidential and proprietary technical documents cannot be dispatched across public cloud networks due to stringent data governance regulations, intellectual property protection mandates, and substantial recurring token costs.

DocuVideo RAG shifts the paradigm by demonstrating that high-precision document comprehension, semantic retrieval, and multi-track presentation video synthesis can be accomplished entirely on client-side commodity hardware with zero external API calls. The technical scope spans:
1. High-fidelity structural PDF parsing and unicode normalization.
2. Context-preserving sliding window chunking with semantic overlap.
3. Dual-mode vector space retrieval combining local ONNX dense embeddings (384-dimensional all-MiniLM-L6-v2) and pure mathematical sparse TF-IDF cosine ranking.
4. Extractive TextRank salience scoring and discourse structuring for deterministic bullet point and speech synthesis.
5. High-definition (1920x1080) visual graphics rendering via programmatic canvas composition.
6. Native thread-safe offline speech synthesis utilizing Windows Speech API (SAPI5).
7. Automated audio-visual timeline alignment and broadcast-ready H.264/AAC video encoding."""

TABLE_OF_CONTENTS_DATA = [
    ("", "Certificate", "ii"),
    ("", "Declaration", "iii"),
    ("", "Acknowledgement", "iv"),
    ("", "Area of Work", "v"),
    ("", "Abstract", "vi"),
    ("1", "Introduction", "1"),
    ("2", "Literature Review & Survey", "4"),
    ("3", "Problem Definition and Objectives", "9"),
    ("4", "Proposed Methodology and Work Description", "11"),
    ("5", "Proposed Algorithms", "18"),
    ("6", "Proposed Flowchart / Block Diagram / DFD", "20"),
    ("7", "Implementation (Tools & Technology Used)", "25"),
    ("8", "Result Discussion and Analysis", "31"),
    ("9", "Conclusion and Future Scope", "37"),
    ("10", "References (IEEE Format)", "39"),
    ("11", "List of Publications", "42"),
    ("12", "Plagiarism & AI Similarity Report", "43"),
]

LIST_OF_FIGURES_DATA = [
    ("1", "High-Level End-to-End System Architecture of DocuVideo RAG", "12"),
    ("2", "Text Normalization and Context-Preserving Sliding Window Chunking", "13"),
    ("3", "Dual-Mode Vector Space Retrieval (ChromaDB ONNX vs. TF-IDF)", "15"),
    ("4", "Extractive TextRank Salience Scoring and Novelty Filtering Workflow", "17"),
    ("5", "1920x1080 High-Definition Presentation Slide Layout Architecture", "18"),
    ("6", "Data Flow Diagram (DFD Level 0 Context Diagram)", "21"),
    ("7", "Data Flow Diagram (DFD Level 1 Detailed Process Flow)", "22"),
    ("8", "Audio-Visual Synchronization and Timeline Assembly Model", "24"),
    ("9", "Latency Breakdown Across Pipeline Execution Stages", "33"),
]

LIST_OF_TABLES_DATA = [
    ("1", "Technical Stack and Architectural Dependencies", "26"),
    ("2", "Algorithmic Comparison: Dense Vector Retrieval vs. Sparse TF-IDF", "16"),
    ("3", "Experimental Benchmark Performance on Academic Research Document", "32"),
    ("4", "Latency Profiling Across Execution Pipeline Stages", "33"),
    ("5", "Feature and Operational Comparison with Cloud-Dependent Systems", "35"),
    ("6", "System Resource Footprint and Utilization Summary", "36"),
]

REFERENCES_DATA = [
    '[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.',
    '[2] R. Mihalcea and P. Tarau, "TextRank: Bringing Order into Text," in Proceedings of the 2004 Conference on Empirical Methods in Natural Language Processing (EMNLP), Barcelona, Spain, pp. 404–411, 2004.',
    '[3] G. Salton and C. Buckley, "Term-weighting approaches in automatic text retrieval," Information Processing & Management, vol. 24, no. 5, pp. 513–523, 1988.',
    '[4] N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), Hong Kong, China, pp. 3982–3992, 2019.',
    '[5] G. Erkan and D. R. Radev, "LexRank: Graph-based lexical centrality as salience in text summarization," Journal of Artificial Intelligence Research, vol. 22, pp. 457–479, 2004.',
    '[6] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp. 333–389, 2009.',
    '[7] Y. A. Malkov and D. A. Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 42, no. 4, pp. 824–836, Apr. 2020.',
    '[8] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention is All You Need," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998–6008, 2017.',
    '[9] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," in Proceedings of NAACL-HLT, Minneapolis, MN, USA, pp. 4171–4186, 2019.',
    '[10] C. D. Manning, P. Raghavan, and H. Schütze, Introduction to Information Retrieval, Cambridge, UK: Cambridge University Press, 2008.',
    '[11] S. Deerwester, S. T. Dumais, G. W. Furnas, T. K. Landauer, and R. Harshman, "Indexing by latent semantic analysis," Journal of the American Society for Information Science, vol. 41, no. 6, pp. 391–407, 1990.',
    '[12] Microsoft Corporation, "Microsoft Speech API (SAPI) 5.4 Overview," MSDN Technical Library, Redmond, WA, Tech. Rep., 2024.',
    '[13] Zulko et al., "MoviePy: A Python module for script-based video editing," Zenodo Software Archive, 2024. [Online]. Available: https://zulko.github.io/moviepy/',
    '[14] T. W. Wiegand, G. J. Sullivan, G. Bjøntegaard, and A. Luthra, "Overview of the H.264/AVC video coding standard," IEEE Transactions on Circuits and Systems for Video Technology, vol. 13, no. 7, pp. 560–576, Jul. 2003.',
    '[15] J. Lin, R. Nogueira, and A. Yates, "Pretrained Transformers for Text Ranking: BERT and Beyond," Synthesis Lectures on Human Language Technologies, Morgan & Claypool, vol. 14, no. 4, pp. 1–325, 2021.',
    '[16] K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu, "BLEU: a method for automatic evaluation of machine translation," in Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL), Philadelphia, PA, USA, pp. 311–318, 2002.',
    '[17] C.-Y. Lin, "ROUGE: A Package for Automatic Evaluation of Summaries," in Text Summarization Branches Out: Proceedings of the ACL-04 Workshop, Barcelona, Spain, pp. 74–81, 2004.',
    '[18] A. Nenkova and K. McKeown, "Automatic Summarization," Foundations and Trends in Information Retrieval, vol. 5, no. 2–3, pp. 103–233, 2011.',
    '[19] H. P. Luhn, "The automatic creation of literature abstracts," IBM Journal of Research and Development, vol. 2, no. 2, pp. 159–165, 1958.',
    '[20] J. Carbonell and J. Goldstein, "The use of MMR, diversity-based reranking for reordering documents and producing summaries," in Proceedings of the 21st Annual International ACM SIGIR Conference, Melbourne, Australia, pp. 335–336, 1998.',
    '[21] Chroma Core Team, "Chroma: The open-source embedding database," GitHub Repository, 2024. [Online]. Available: https://github.com/chroma-core/chroma',
    '[22] ONNX Runtime Developers, "ONNX Runtime: Cross-platform, high performance ML inferencing and training accelerator," Linux Foundation, 2024. [Online]. Available: https://onnxruntime.ai/',
    '[23] Streamlit Inc., "Streamlit: The fastest way to build and share data apps," Snowflake Inc., 2024. [Online]. Available: https://streamlit.io/',
    '[24] J. S. Clark, "Pillow: The friendly PIL fork for Python image processing," Python Software Foundation, 2024. [Online]. Available: https://python-pillow.org/',
    '[25] J. H. Park and S. B. Cho, "Automatic generation of presentation slides from scientific papers using natural language processing," Expert Systems with Applications, vol. 116, pp. 382–391, 2019.'
]

print("Report content data loaded successfully.")
