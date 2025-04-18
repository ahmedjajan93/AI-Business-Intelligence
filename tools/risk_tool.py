from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os 
import re
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

risk_prompt = PromptTemplate(
    input_variables=["company", "text"],
    template="""
    Analyze the following text from {company}'s website and identify business risks.

    Categorize them into:
    - Financial
    - Legal
    - Operational
    - Technical
    - Market

    For each category, provide:
    - A 1–2 sentence summary of key risk(s)
    - A severity score: Low, Medium, or High

    Format (exactly like this):
    Financial Risk: <summary> (Severity: <Low/Medium/High>)
    Legal Risk: <summary> (Severity: <Low/Medium/High>)
    ...

    Text:
    \"\"\"{text}\"\"\"
    """
)

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re

risk_prompt = PromptTemplate(
    input_variables=["company", "text"],
    template="""
    Analyze the following text from {company}'s website and identify business risks.

    Categorize them into:
    - Financial
    - Legal
    - Operational
    - Technical
    - Market

    For each category, provide:
    - A 1–2 sentence summary of key risk(s)
    - A severity score: Low, Medium, or High

    Format (exactly like this):
    Financial Risk: <summary> (Severity: <Low/Medium/High>)
    Legal Risk: <summary> (Severity: <Low/Medium/High>)
    ...

    Text:
    \"\"\"{text}\"\"\"
    """
)

def analyze_risks_with_severity(company: str, text: str) -> dict:
   # Initialize LLM
    llm = ChatOpenAI(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                base_url="https://openrouter.ai/api/v1",)
    chain = LLMChain(llm=llm, prompt=risk_prompt)
    result = chain.run(company=company, text=text)

    # Clean up and extract risk summaries + severity
    pattern = r"(\w+?) Risk:\s*(.*?)(?:\s*\(Severity:\s*(Low|Medium|High)\))"
    matches = re.findall(pattern, result, re.DOTALL)

    severity_map = {"Low": 1, "Medium": 2, "High": 3}
    risk_data = {}

    for category, summary, severity in matches:
        cat = category.strip().capitalize()
        risk_data[cat] = {
            "summary": summary.strip().replace('\n', ' '),
            "severity": severity.strip(),
            "score": severity_map.get(severity.strip(), 0)
        }

    return risk_data

