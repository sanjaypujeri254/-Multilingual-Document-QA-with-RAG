import streamlit as st
from retriever import load_documents, create_vector_store
from src.generator import get_qa_chain
import speech_recognition as sr
from gtts import gTTS
import os
import csv
from datetime import datetime
from langdetect import detect
from elasticsearch import Elasticsearch

# Initialize Elasticsearch
es = Elasticsearch("http://elasticsearch:9200")

# Ensure log directory exists
os.makedirs("query_logs", exist_ok=True)
LOG_FILE = "query_logs/query_history.csv"

# Load and index documents
docs = load_documents("data/sample_docs")
vectordb = create_vector_store(docs)
retriever = vectordb.as_retriever()
qa_chain = get_qa_chain(retriever)

# Voice Input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak your question...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        return text
    except:
        return "Sorry, couldn't recognize your speech."

# Log query to CSV and Elasticsearch
def log_query(user_input, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, user_input, answer])

    es.index(index="qa_history", document={
        "timestamp": timestamp,
        "question": user_input,
        "answer": answer
    })

# Text/Voice input choice
st.title("📄 Multilingual RAG Document QA")
query_mode = st.radio("Choose input mode:", ("Text", "Voice"))

if query_mode == "Text":
    user_input = st.text_input("Ask your question:")
else:
    if st.button("🎙️ Record Question"):
        user_input = voice_input()
        st.write(f"You said: **{user_input}**")

# Process and answer
if st.button("🔍 Get Answer"):
    if user_input:
        result = qa_chain.run(user_input)
        st.write("**Answer:**", result)

        # Log query and answer
        log_query(user_input, result)

        # Detect language for TTS
        try:
            detected_lang = detect(result)
        except:
            detected_lang = "en"

        tts = gTTS(text=result, lang=detected_lang if detected_lang != 'unknown' else 'en')
        tts.save("answer.mp3")
        os.system("start answer.mp3")

    else:
        st.warning("Please enter or speak a question.")
