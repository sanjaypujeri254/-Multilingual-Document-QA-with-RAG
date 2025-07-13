# Multilingual Document QA with RAG

An AI-powered multilingual document question answering system using **Retrieval-Augmented Generation (RAG)** architecture with **LangChain**, **FAISS**, **Streamlit**, and **Elasticsearch**.  
It allows users to query uploaded **PDF, DOCX, and TXT documents** via **text or voice inputs** — supporting **automatic language detection** and **text-to-speech (TTS) responses**.

---

## How It Works

- The application reads **PDF, DOCX, and TXT documents** and splits them into smaller text chunks.
- Each chunk is converted into a vector embedding using **multilingual Sentence-Transformer models**.
- Embeddings are stored in a **FAISS vector database**.
- On receiving a query (via text or voice), it finds **semantically similar document chunks**.
- Relevant chunks are passed to **OpenAI GPT-3.5 via LangChain** to generate context-aware answers.
- The answer is spoken back using **Text-to-Speech (TTS)** in the detected language.
- Every query-answer interaction is **logged into Elasticsearch** and visualized using **Kibana dashboards**.
- The entire multi-service application is **containerized with Docker Compose** for simple deployment.

---

## Folder Structure

```
multilingual_enterprise_doc_qa_rag/
│
├── data/
│   └── sample_docs/        # PDF, DOCX, TXT files for QA
│
├── query_logs/             # CSV logs of query-answer history
│
├── src/
│   ├── app.py              # Streamlit application UI
│   ├── retriever.py        # Document loader & FAISS vector store
│   └── generator.py        # LangChain QA chain handler
│
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container config for the app
├── docker-compose.yml      # Multi-service Docker Compose config
└── README.md               # Project documentation (this file)
```

---

## Installation

### Install Python packages locally:
```bash
pip install -r requirements.txt
```

### Usage

#### Local (without Docker)

Place your documents inside:
```bash
data/sample_docs/
```

Run the Streamlit app:
```bash
streamlit run src/app.py
```

(Optional) Run Elasticsearch:
```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.1
```

Visit the app in your browser:
```
http://localhost:8501
```

#### Full Docker Deployment

Run the complete stack:
```bash
docker-compose up --build
```

Access services:
- **App:** [http://localhost:8501](http://localhost:8501)
- **Kibana:** [http://localhost:5601](http://localhost:5601)
- **Elasticsearch API:** [http://localhost:9200](http://localhost:9200)

---

## Features

- Multilingual PDF, DOCX, and TXT document ingestion
- Retrieval-Augmented Generation (RAG) QA using LangChain and FAISS
- Text and voice query input with automatic language detection
- TTS voice response generation
- Query-answer logs stored in Elasticsearch, visualized via Kibana
- Docker Compose multi-service deployment

---

## Future Work

- Add support for web-based document upload UI
- Integrate Hugging Face LLM backends
- Build query analytics and usage dashboards
- Implement user authentication and session tracking
