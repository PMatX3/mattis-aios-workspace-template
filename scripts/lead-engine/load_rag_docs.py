"""
RAG Document Loader — AIOS Lead Engine

Loads business context documents into Open Brain (or any vector store) so the
Vapi voice qualifier can answer questions accurately with source citations.

Usage:
    python scripts/lead-engine/load_rag_docs.py          # Load all docs
    python scripts/lead-engine/load_rag_docs.py --check  # Check what's loaded

CUSTOMISE: Replace the RAG_DOCUMENTS list below with your own knowledge base.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

# CUSTOMISE THIS — replace with your own knowledge base content
# Each entry has a topic and one or more chunks. Each chunk has a label and content.
# The voice agent retrieves these by topic + semantic search to answer caller questions.
RAG_DOCUMENTS = [
    {
        "file": "context/business-info.md",
        "topic": "company-overview",
        "chunks": [
            {
                "label": "What [Your Agency] does",
                "content": """[REPLACE WITH YOUR CONTENT]

Describe what your business does, who you serve, and what your typical work looks like.
Keep it 3-5 sentences. The voice agent uses this to answer "what does [agency] do?".""",
            },
            {
                "label": "How we work with clients",
                "content": """[REPLACE WITH YOUR CONTENT]

Describe your delivery process, what working with you looks like, what tools you use.
The voice agent uses this to answer process and tooling questions.""",
            },
            {
                "label": "Company details",
                "content": """[REPLACE WITH YOUR CONTENT]

Company name, founder name, location, team size, stage, website.""",
            },
        ],
    },
    {
        "topic": "delivery-process",
        "chunks": [
            {
                "label": "Standard delivery process",
                "content": """[REPLACE WITH YOUR CONTENT]

Walk through your typical project lifecycle: discovery, scoping, build, UAT, handover.
Mention typical timelines (e.g. 2-4 weeks).""",
            },
        ],
    },
    {
        "topic": "faqs",
        "chunks": [
            {
                "label": "Common questions about working with us",
                "content": """[REPLACE WITH YOUR CONTENT — example FAQ structure below]

Q: How long does a typical build take?
A: [Your answer]

Q: What tech stack do you use?
A: [Your answer]

Q: What happens after the build?
A: [Your answer]

Q: What if the build doesn't work?
A: [Your answer]""",
            },
        ],
    },
    {
        "topic": "qualification-criteria",
        "chunks": [
            {
                "label": "Who we work best with",
                "content": """[REPLACE WITH YOUR CONTENT]

Describe your ideal client profile.

We're not the right fit for:
- [Disqualifier 1]
- [Disqualifier 2]
- [Disqualifier 3]""",
            },
        ],
    },
]


def chunk_and_load():
    """Load all RAG documents into your vector store.

    NOTE: This template uses Open Brain as the vector store. Replace the
    `capture` function with your store of choice (Pinecone, Weaviate, Supabase
    pgvector, etc.) if needed.
    """
    try:
        from open_brain import capture, search_text, is_configured
    except ImportError:
        print("open_brain module not found. Replace this with your vector store of choice.")
        print("This script is a template — wire it to Pinecone, Weaviate, Supabase pgvector,")
        print("or whichever vector store backs your voice agent's RAG.")
        sys.exit(1)

    if not is_configured():
        print("ERROR: Vector store not configured. Check .env credentials.")
        sys.exit(1)

    total = 0
    for doc in RAG_DOCUMENTS:
        topic = doc["topic"]
        file_ref = doc.get("file", "internal")
        print(f"\nLoading: {topic} (from {file_ref})")

        for chunk in doc["chunks"]:
            label = chunk["label"]
            content = f"[{label}]\n\n{chunk['content']}"

            result = capture(
                content=content,
                thought_type="reference",
                topic=f"lead-engine-rag:{topic}",
            )

            if result:
                print(f"  Loaded: {label}")
                total += 1
            else:
                print(f"  FAILED: {label}")

    print(f"\nDone. Loaded {total} chunks into the vector store.")


def check_loaded():
    """Check what RAG documents are currently loaded."""
    try:
        from open_brain import search_text, is_configured
    except ImportError:
        print("open_brain module not found.")
        sys.exit(1)

    if not is_configured():
        print("ERROR: Vector store not configured.")
        sys.exit(1)

    results = search_text("lead-engine-rag", limit=50)
    if not results:
        print("No lead-engine RAG documents found.")
        return

    print(f"Found {len(results)} lead-engine RAG chunks:\n")
    for r in results:
        topic = r.get("topic", "unknown")
        content_preview = r.get("content", "")[:80]
        created = r.get("created_at", "unknown")
        print(f"  [{topic}] {content_preview}... (created: {created})")


def main():
    parser = argparse.ArgumentParser(description="Load RAG docs into vector store")
    parser.add_argument("--check", action="store_true", help="Check what's loaded")
    args = parser.parse_args()

    if args.check:
        check_loaded()
    else:
        chunk_and_load()


if __name__ == "__main__":
    main()
