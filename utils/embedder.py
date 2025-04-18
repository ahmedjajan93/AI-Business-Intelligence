# 📁 File: utils/embedder.py
from langchain.embeddings import HuggingFaceEmbeddings

def get_embedder():
    return HuggingFaceEmbeddings()
