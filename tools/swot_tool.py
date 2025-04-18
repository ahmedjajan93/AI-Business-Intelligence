# 📁 File: tools/swot_tool.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def generate_swot(company_name, content):
    prompt = PromptTemplate.from_template("""
    Based on the following content about {company_name}, create a detailed SWOT analysis.

    Content: {content}

    Format:
    Strengths:
    - ...
    Weaknesses:
    - ...
    Opportunities:
    - ...
    Threats:
    - ...
    """)
  # Initialize LLM
    llm = ChatOpenAI(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                base_url="https://openrouter.ai/api/v1",)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(company_name=company_name, content=content[:3000])
