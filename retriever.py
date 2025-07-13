from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_documents(directory):
    docs = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        elif filename.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
            docs.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
            docs.extend(loader.load())
    return docs

def create_vector_store(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectordb = FAISS.from_documents(chunks, embedding_model)
    return vectordb
