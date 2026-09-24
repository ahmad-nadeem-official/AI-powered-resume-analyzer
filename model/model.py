from langchain_groq import ChatGroq
from output.output import OP
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


ai = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1,
    max_tokens=None,
    # max_retries=3,
    # reasoning_format= "parsed",
    # rate_limiter=None).
)

aii = ai.with_structured_output(OP)