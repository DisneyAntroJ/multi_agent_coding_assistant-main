from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json


# 🔐 Load environment variables
load_dotenv()


# 🔑 Get Groq API key
api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in .env file")


# 🤖 Initialize LLM (Groq)
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)


# 🏗️ Architect Agent
def architect_agent(plan: dict):
    prompt = f"""
    You are a software architect.


    Based on this project plan, generate a file structure.


    Return ONLY valid JSON.
    Do NOT include markdown (no ```).


    Format:
    {{
        "files": ["file1", "file2", "file3"]
    }}


    Plan:
    {plan}
    """


    response = llm.invoke(prompt).content




    # 🧹 Clean markdown if present
    cleaned = response.replace("```json", "").replace("```", "").strip()


    # 🔧 Convert to JSON
    try:
        data = json.loads(cleaned)
    except:
        print("⚠️ RAW RESPONSE:")
        print(response)
        data = {"error": "Invalid JSON output"}


    return data




# 🚀 Test
if __name__ == "__main__":
    sample_plan = {
        "project_name": "calculator_web_app",
        "features": [
            "addition",
            "subtraction",
            "multiplication",
            "division"
        ],
        "tech_stack": ["HTML", "CSS", "JavaScript"]
    }


    result = architect_agent(sample_plan)


    print("\n✅ Architect Output:")
    print(json.dumps(result, indent=4))