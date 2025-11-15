## knowl

knowl -> Knowledge Discovery on Obsidian vaults with RAG System.

## Objective:

Make a knowledge discovery platform that ingests our local markdown files as input
and provide semantic Q\&A , search and summarization over the notes.

- Privacy is a big issue and for that reason we are using open source models and vector databases.

## High Level Overview:

- **Controlled corpus** (local `.md` files)
- **Simpler ingestion pipeline** (just parse markdown, keep headings/links)
- **Clear use case** (semantic Q\&A, search, summarization over your notes)

## 🎯 System Overview (Markdown-only RAG)

**Flow:**
Markdown files → Parse + Chunk → Embeddings + Metadata → Vector Store → Retrieval + Context Assembly → LLM Answer → UI/API

---

## 1. Ingestion & Parsing

- Traverse your Obsidian vault (just a directory of `.md` files).
- Extract:

  - File name (as document ID)
  - Headings and section hierarchy (to keep structure)
  - Outgoing links (`[[note]]`) and tags (`#tag`) for metadata

- Convert Markdown → plain text but keep links/headings in metadata.

👉 Tools:

- [`markdown-it-py`](https://markdown-it-py.readthedocs.io/) or [`mistune`](https://github.com/lepture/mistune) for parsing
- Python standard `pathlib` for walking the vault

---

## 2. Chunking

- Split by **headings** (prefer hierarchical chunks).
- If a section is large, further chunk by \~500 tokens with \~20% overlap.
- Store: `doc_id`, `section_heading`, `content`, `links`, `tags`.

---

## 3. Embeddings + Index

- Use sentence-transformers (`all-MiniLM-L6-v2` or `multi-qa-MiniLM`) for local lightweight setup.
- Store embeddings + metadata in a vector DB:

  - For local dev: FAISS (super simple, single-file DB).
  - For more features: Qdrant (Docker, REST + Python client).

---

## 4. Retrieval

- User query → embed → top-k nearest chunks.
- Optionally filter by tags/linked notes (e.g., only notes under `#research`).
- Combine with **Maximal Marginal Relevance (MMR)** to avoid redundant chunks.

---

## 5. Context Assembly

- Build a context prompt:

  - Include chunk text
  - Include metadata (filename, heading, links) for citation

- Example format:

  ```
  [Doc: research_methods.md | Section: Sampling Techniques]
  Text: "In random sampling, each unit has equal chance..."
  ```

---

## 6. Answer Generation

- Send query + retrieved context to an LLM.
- LLM returns answer **with citations** in `[Doc: section]` format.
- Models:

  - Easy start: OpenAI `gpt-4o-mini` (fast + cheap).
  - Local: `mistral-7b-instruct` with `vLLM` or `llama.cpp` if you want offline.

---

## 7. Interface

- **CLI/Terminal** (quick MVP):

  ```bash
  python rag.py "What are my notes on transformers in NLP?"
  ```

  Returns answer + source files.
