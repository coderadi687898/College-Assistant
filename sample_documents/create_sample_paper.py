"""
Sample Academic PDF Generator
Generates a multi-page, realistic academic conference paper using standard PDF specification.
Requires zero external dependencies.
"""

import os

def generate_sample_research_paper(output_path="sample_documents/sample_research_paper.pdf"):
    """Creates a realistic 3-page academic research paper PDF."""
    
    # Text contents for 3 pages
    page1_lines = [
        "Autonomous Edge Computing: Architecture, Protocols, and Resilience",
        "Department of Computer Science & Engineering - Technical Research Report",
        "",
        "ABSTRACT",
        "Edge computing addresses latency and bandwidth limitations by executing data processing",
        "closer to edge sensors rather than depending exclusively on centralized cloud data centers.",
        "In this study, we present an autonomous edge computing architecture tailored for high-frequency",
        "Internet of Things (IoT) workloads. Our approach introduces localized state arbitration, zero-loss",
        "fault recovery, and lightweight telemetry caching. Benchmarks across 50 simulated edge clusters",
        "demonstrate a 68 percent reduction in packet transmission latency and a 42 percent savings in",
        "backhaul network bandwidth compared to traditional cloud-only ingestion models.",
        "",
        "1. INTRODUCTION AND MOTIVATION",
        "The exponential proliferation of smart infrastructure, autonomous vehicles, and industrial sensors",
        "has overwhelmed conventional cloud storage pipelines. Transmitting raw telemetry across wide-area",
        "networks introduces unpredictable network jitter, high transit costs, and vulnerabilities to intermittent",
        "connectivity failures. Edge computing bridges this gap by provisioning decentralized micro-clusters.",
        "",
        "By filtering and aggregating telemetry at the ingress gateway, edge systems insulate critical control loops",
        "from wide-area communication drops. However, deploying computation to untrusted, resource-constrained",
        "nodes introduces formidable challenges in decentralized data synchronization and fault tolerance.",
        "",
        "This project outlines an algorithmic framework for edge self-orchestration that enables edge clusters",
        "to sustain localized processing even during extended wide-area network partitions."
    ]
    
    page2_lines = [
        "2. SYSTEM ARCHITECTURE AND CORE MODULES",
        "The proposed system consists of three hierarchical layers: Sensing, Edge Gateway, and Cloud Core.",
        "",
        "A. Sensor Ingestion Layer",
        "IoT field devices interface with local micro-gateways using lightweight telemetry protocols such as MQTT",
        "and CoAP. Ingestion buffers utilize ring-buffer queues to prevent memory overflow during telemetry spikes.",
        "",
        "B. Edge Processing Gateway (Fog Layer)",
        "The gateway layer hosts lightweight containers responsible for real-time anomaly detection, local rule",
        "enforcement, and sliding-window statistical aggregation. A local storage engine maintains time-series",
        "snapshots to handle transient network disconnects without data degradation.",
        "",
        "C. Centralized Cloud Coordination Core",
        "The cloud layer acts as a global coordinator. It aggregates summarized metrics from distributed edge clusters,",
        "coordinates global policy updates, and conducts deep historical auditing using scalable data lakes.",
        "",
        "3. RETRIEVAL AND REPLICATION PROTOCOLS",
        "Our framework implements an epoch-based gossip replication protocol. Edge nodes maintain vector clocks",
        "to track causality between concurrent data events. When a network partition is healed, nodes reconcile",
        "conflicting updates using deterministic CRDT (Conflict-Free Replicated Data Type) state merging.",
        "This ensures eventual consistency without requiring centralized global locking overhead."
    ]
    
    page3_lines = [
        "4. EXPERIMENTAL EVALUATION AND RESULTS",
        "To evaluate our architecture, we conducted rigorous benchmarks across a distributed testbed of 50 virtualized",
        "Raspberry Pi nodes connected to a central server with simulated WAN latency variations (10ms to 250ms).",
        "",
        "- Latency Reduction: End-to-end response times dropped from 240ms in cloud models to 28ms under local edge processing.",
        "- Network Bandwidth Savings: Ingress bandwidth consumption fell by 42.4 percent due to localized feature aggregation.",
        "- Fault Tolerance: Nodes demonstrated uninterrupted operation during a simulated 45-minute cloud link partition.",
        "- Recovery Time: Upon reconnection, full vector state synchronization completed in under 1.8 seconds.",
        "",
        "5. CONCLUSION AND FUTURE SCOPE",
        "This research validates that decentralized edge architectures significantly outperform traditional centralized",
        "architectures in latency-sensitive industrial applications. Local telemetry processing protects real-time control",
        "loops while drastically curbing cloud transit overhead.",
        "",
        "Future enhancements will investigate lightweight machine learning inference at the edge using quantization,",
        "energy-aware dynamic load balancing, and zero-knowledge cryptographic verification for edge-to-cloud streams.",
        "",
        "ACKNOWLEDGEMENT",
        "This research was conducted as part of the College Minor Project in Advanced Distributed Systems."
    ]

    def make_stream(lines):
        stream_cmds = ["BT", "/F1 14 Tf", "50 740 Td"]
        is_first = True
        for line in lines:
            safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            if is_first:
                stream_cmds.append(f"({safe_line}) Tj")
                stream_cmds.append("/F2 10 Tf")
                is_first = False
            else:
                stream_cmds.append("0 -18 Td")
                if line.isupper() and len(line) < 40 and not line.startswith("-"):
                    stream_cmds.append("/F1 11 Tf")
                    stream_cmds.append(f"({safe_line}) Tj")
                    stream_cmds.append("/F2 10 Tf")
                else:
                    stream_cmds.append(f"({safe_line}) Tj")
        stream_cmds.append("ET")
        return "\n".join(stream_cmds).encode('latin-1')

    s1 = make_stream(page1_lines)
    s2 = make_stream(page2_lines)
    s3 = make_stream(page3_lines)

    # Build PDF binary
    parts = []
    parts.append(b"%PDF-1.4\n")
    
    # 1 0 obj: Catalog
    parts.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2 0 obj: Pages
    parts.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R] /Count 3 >>\nendobj\n")
    
    # Fonts
    # 6 0 obj: Font Bold
    parts.append(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    # 7 0 obj: Font Regular
    parts.append(b"7 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    
    # Pages 3, 4, 5
    parts.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 8 0 R /Resources << /Font << /F1 6 0 R /F2 7 0 R >> >> >>\nendobj\n")
    parts.append(b"4 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 9 0 R /Resources << /Font << /F1 6 0 R /F2 7 0 R >> >> >>\nendobj\n")
    parts.append(b"5 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 10 0 R /Resources << /Font << /F1 6 0 R /F2 7 0 R >> >> >>\nendobj\n")

    # Streams 8, 9, 10
    parts.append(f"8 0 obj\n<< /Length {len(s1)} >>\nstream\n".encode('latin-1') + s1 + b"\nendstream\nendobj\n")
    parts.append(f"9 0 obj\n<< /Length {len(s2)} >>\nstream\n".encode('latin-1') + s2 + b"\nendstream\nendobj\n")
    parts.append(f"10 0 obj\n<< /Length {len(s3)} >>\nstream\n".encode('latin-1') + s3 + b"\nendstream\nendobj\n")

    # Compute xref
    # Calculate byte offsets
    body = b"".join(parts)
    offsets = [0]
    
    # We have objects 1 to 10
    obj_markers = [
        b"1 0 obj", b"2 0 obj", b"3 0 obj", b"4 0 obj", b"5 0 obj",
        b"6 0 obj", b"7 0 obj", b"8 0 obj", b"9 0 obj", b"10 0 obj"
    ]
    
    obj_positions = {}
    for i, marker in enumerate(obj_markers, 1):
        pos = body.find(marker)
        obj_positions[i] = pos
        
    xref_offset = len(body)
    xref_lines = [b"xref\n0 11\n0000000000 65535 f \n"]
    for i in range(1, 11):
        pos = obj_positions[i]
        xref_lines.append(f"{pos:010d} 00000 n \n".encode('latin-1'))
    
    trailer = f"trailer\n<< /Size 11 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode('latin-1')
    
    final_pdf = body + b"".join(xref_lines) + trailer
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(final_pdf)
    print(f"Generated sample research paper at: {output_path} ({len(final_pdf)} bytes)")
    return output_path

if __name__ == "__main__":
    generate_sample_research_paper()
