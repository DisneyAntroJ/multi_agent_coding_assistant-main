from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import RateLimitError
import os
import time
import json


# 🔐 Load env
load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found")


# 🤖 LLM Setup
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="openai/gpt-oss-120b",
    temperature=0
)


def write_file(project_name, file_name, content):
    file_path = os.path.join(project_name, file_name)

    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(file_path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


    print(f"✅ Created: {file_name}")




# 👨‍💻 Coder Agent
def coder_agent(plan: dict, architecture: dict):
    project_name = plan["project_name"].lower().replace(" ", "_")
    files = architecture["files"]


    for file in files:
        print(f"⚡ Generating {file}...")


        prompt = f"""
        You are a professional software developer.


        Generate complete code for the file: {file}


        Project details:
        {plan}


        Rules:
        - Return ONLY code
        - No explanations
        - No markdown (no ```)


        """


      try:
    response = llm.invoke(prompt).content

except RateLimitError:
    time.sleep(10)

    try:
        response = llm.invoke(prompt).content

    except RateLimitError:
        return {
            "error": "Groq rate limit reached. Please wait a minute and try again."
        }
        # Clean unwanted markdown if present
        cleaned = response.replace("```", "").strip()


        write_file(project_name, file, cleaned)


    return f"🎉 Project '{project_name}' created successfully!"




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


    sample_architecture = {
        "files": [
            "index.html",
            "style.css",
            "script.js",
            "addition.js",
            "subtraction.js",
            "multiplication.js",
            "division.js"
        ]
    }


    result = coder_agent(sample_plan, sample_architecture)
    print(result)



