"""
Aegis grounded Q&A: ask a question about the EU AI Act and get an answer
that quotes the retrieved passages, with page citations.

Reads the Chroma index built in Week 2 (build_index.py), retrieves the
top-k most relevant chunks for a question, sends those chunks plus the
question to Groq, and prints the answer. The model is constrained to use
only the provided passages. If the passages don't cover the question, it
says so rather than making something up.

Run from the project root:
    python src/aegis/grounded_qa.py
"""

from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq
from llama_index.core import VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


# --- Configuration ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "ai_act_v1"

# Must match the model used in build_index.py. If they differ, retrieval
# breaks silently because the question vector lives in a different space
# than the indexed chunks.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Llama 3.3 70B on Groq. Switch to llama-3.1-8b-instant for faster/cheaper
# iteration if the 70B latency becomes a bottleneck during development.
GROQ_MODEL = "llama-3.3-70b-versatile"

# Five chunks of context. Tunable. The Week 8 evaluation harness will
# decide whether 3, 5, or 10 retrieves the best accuracy.
TOP_K = 5

WRAP_WIDTH = 88


# --- System prompt ----------------------------------------------------------
# Instructions to the model, not human-facing copy.

SYSTEM_PROMPT = """You are a research assistant for the EU AI Act. Answer questions using ONLY the passages provided below.

Rules:
1. Quote or closely paraphrase from the passages. Do not invent text.
2. After each factual claim, cite the page in square brackets like [page 42].
3. If the passages do not contain enough information, say so plainly. Do not guess. Do not fall back on general knowledge.
4. Do not provide legal advice. End every answer with the disclaimer line below.
5. Be concise. Two or three short paragraphs is usually enough.

Disclaimer line, included verbatim at the end of every answer:
"This is decision-support, not legal advice. Verify with qualified counsel."
"""


def load_index() -> VectorStoreIndex:
    """Open the Chroma collection built in Week 2."""
    print(f"Loading Chroma collection '{COLLECTION_NAME}' from {CHROMA_DB_PATH}...")
    db = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    collection = db.get_collection(COLLECTION_NAME)
    print(f"  Collection has {collection.count()} chunks.\n")

    print(f"Loading embedding model {EMBEDDING_MODEL}...")
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.embed_model = embed_model

    vector_store = ChromaVectorStore(chroma_collection=collection)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def retrieve_chunks(index: VectorStoreIndex, question: str, top_k: int = TOP_K):
    """Return the top-k most relevant chunks for the question."""
    retriever = index.as_retriever(similarity_top_k=top_k)
    return retriever.retrieve(question)


def build_user_prompt(question: str, retrieved_nodes) -> str:
    """Format question + retrieved chunks into a single user message."""
    chunks_text = []
    for i, node in enumerate(retrieved_nodes, start=1):
        page = node.metadata.get("page", "?")
        text = node.text.replace("\n", " ").strip()
        chunks_text.append(f"[Passage {i}, page {page}]\n{text}")

    chunks_block = "\n\n".join(chunks_text)

    return (
        f"Question: {question}\n\n"
        f"Passages from the EU AI Act:\n\n"
        f"{chunks_block}\n\n"
        f"Answer the question using only these passages."
    )


def ask(client: Groq, question: str, retrieved_nodes) -> str:
    """Send question + chunks to Groq, return the generated answer."""
    user_prompt = build_user_prompt(question, retrieved_nodes)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,  # low temperature for factual, low-creativity answers
        max_tokens=800,
    )
    return response.choices[0].message.content


def print_chunks(retrieved_nodes) -> None:
    """Show retrieved chunks so the user can verify what the model saw."""
    print("Retrieved passages:")
    print("-" * WRAP_WIDTH)
    for i, node in enumerate(retrieved_nodes, start=1):
        page = node.metadata.get("page", "?")
        score = node.score if node.score is not None else 0.0
        snippet = node.text.replace("\n", " ").strip()
        snippet = textwrap.shorten(snippet, width=300, placeholder=" [...]")
        wrapped = textwrap.fill(snippet, width=WRAP_WIDTH)
        print(f"\n[{i}] page {page}, similarity {score:.3f}")
        print(wrapped)
    print("-" * WRAP_WIDTH)
    print()


def main() -> int:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY is not set. Add it to your .env file.")
        return 1

    client = Groq(api_key=api_key)

    # Three test questions covering different parts of the Act.
    questions = [
        "What does Article 13 require for transparency in high-risk AI systems?",
        "What are the obligations on providers of general-purpose AI models?",
        "Which AI practices are prohibited under Article 5?",
    ]

    index = load_index()

    for question in questions:
        print("=" * WRAP_WIDTH)
        print(f"QUESTION: {question}")
        print("=" * WRAP_WIDTH)
        print()

        chunks = retrieve_chunks(index, question)
        print_chunks(chunks)

        print("Answer:")
        print("-" * WRAP_WIDTH)
        answer = ask(client, question, chunks)
        for paragraph in answer.split("\n\n"):
            print(textwrap.fill(paragraph, width=WRAP_WIDTH))
            print()

    print("Grounded Q&A is working end to end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
