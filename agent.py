# 📁 File: agent.py
from utils.embedder import get_embedder
from utils.faiss_utils import create_faiss_db
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os 
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def build_qa_chain(docs):
    embeddings = get_embedder()
    vectordb = create_faiss_db(docs, embeddings)
    retriever = vectordb.as_retriever()
    
# Initialize LLM
    llm = ChatOpenAI(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                base_url="https://openrouter.ai/api/v1",)

    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
