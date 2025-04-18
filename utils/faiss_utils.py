# 📁 File: utils/faiss_utils.py
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_faiss_db(docs, embeddings):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return FAISS.from_documents(chunks, embeddings)
