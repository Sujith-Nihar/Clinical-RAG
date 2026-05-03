# ClinicalQA-RAG

ClinicalQA-RAG is a RAG-powered medical document question-answering system. It allows users to upload clinical PDFs or text documents, ask natural language questions, and receive grounded answers with source attribution from the uploaded content.

The system is designed to make clinical document understanding faster, more transparent, and easier to verify by combining document retrieval with Gemini-powered embeddings and answer generation.

---

## Features

- Upload clinical PDF or text documents
- Automatically extract and chunk document content
- Generate document embeddings using Gemini Embeddings
- Store and search document chunks using FAISS
- Ask natural language questions about uploaded documents
- Generate grounded answers using Gemini
- Return source-backed responses with document attribution
- Simple React frontend for document upload and Q&A
- FastAPI backend for ingestion, retrieval, and answer generation

---

## Tech Stack

### Frontend

- React
- Tailwind CSS
- Vercel for deployment

### Backend

- FastAPI
- Railway for deployment
- Python

### AI / RAG Pipeline

- Gemini Embedding Model for vector embeddings
- FAISS for vector search
- Gemini LLM for answer generation

---

## Project Structure

```text
ClinicalQA-RAG/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── .env.example
│   └── ...
│
└── README.md
