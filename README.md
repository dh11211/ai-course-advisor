AI Course Advisor (RAG Agent)

A Retrieval-Augmented Generation (RAG) agent designed to assist University of Melbourne students with complex course planning queries. It parses unstructured university handbook data into queryable vector embeddings to provide accurate, context-aware responses regarding prerequisites and degree structures.

Core Architecture

Backend: Python (FastAPI/Flask), OpenAI API

Data Engineering: Vector Embeddings (FAISS/ChromaDB) for semantic search over handbook data.

Frontend: React (Vite)

Validation: Reflexive prompting layer to minimize hallucination rates and verify course codes against degree logic.

Key Features

Handbook Parsing: Ingests raw text/PDF data from the university handbook (data/course_handbook.txt) and chunks it for vector storage.

Semantic Retrieval: Uses cosine similarity to find relevant course rules before generating an answer.

Hallucination Mitigation: Implements a "reflexive" step where the model cross-references its generated answer with the retrieved context before displaying it to the user.

Setup & Installation

Backend

cd backend
pip install -r requirements.txt
python main.py


Frontend

cd frontend
npm install
npm run dev


Status

Current Phase: MVP (Minimum Viable Product).

Next Steps: Integration of multi-year degree planning logic and user session persistence.