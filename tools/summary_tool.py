# 📁 File: tools/summary_tool.py
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
import os 
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def summarize_docs(docs: list[Document]) -> str:
    """
    Summarize a list of LangChain Documents into a concise, high-level summary.
    """
    if not docs:
        return "No documents available for summarization."

    # Initialize LLM
    llm = ChatOpenAI(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                base_url="https://openrouter.ai/api/v1",)

    chain = load_summarize_chain(llm, chain_type="stuff")

    try:
        summary = chain.run(docs)
        return summary
    except Exception as e:
        return f"Failed to generate summary: {e}"
