from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import RateLimitError
import os
import time


# 🔐 Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found")


# 🤖 LLM Setup
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="openai/gpt-oss-20b",
    temperature=0
)


# 📁 Write generated files
def write_file(project_name, file_name, content):
    file_path = os.path.join(project_name, file_name)

    # Create folders automatically
    parent_dir = os.path.dirname(file_path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: {file_name}")


# 👨‍💻 Coder Agent
def coder_agent(plan: dict, architecture: dict):

    project_name = plan["project_name"].lower().replace(" ", "_")

    # Make sure architect returned files
    if "files" not in architecture:
        return {
            "error": "Architect did not return a valid file list.",
            "architecture": architecture
        }

    files = architecture["files"]

    for file in files:

        print(f"⚡ Generating {file}...")

        prompt = f"""
You are a professional senior software developer.

Generate complete working code for this file:

{file}

PROJECT PLAN:
{plan}

PROJECT ARCHITECTURE:
{architecture}

Rules:
- Return ONLY the contents of the requested file.
- Do not include explanations.
- Do not include markdown.
- Do not include ``` or ```python.
- Generate complete working code.
- Make sure the code matches the project architecture.
"""

        try:
            response = llm.invoke(prompt).content

        except RateLimitError:
            print("⚠️ Rate limit reached. Waiting 5 seconds...")
            time.sleep(5)

            try:
                response = llm.invoke(prompt).content

            except RateLimitError:
                return {
                    "error": "Groq rate limit reached. Please wait about one minute and try again."
                }

        # Clean markdown if the model accidentally adds it
        cleaned = response.replace("```python", "")
        cleaned = cleaned.replace("```html", "")
        cleaned = cleaned.replace("```css", "")
        cleaned = cleaned.replace("```javascript", "")
        cleaned = cleaned.replace("```js", "")
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

        write_file(
            project_name,
            file,
            cleaned
        )

    # IMPORTANT: this must be OUTSIDE the for loop
    return f"🎉 Project '{project_name}' created successfully!"


# 🚀 Local Test
if __name__ == "__main__":

    sample_plan = {
        "project_name": "calculator_web_app",
        "features": [
            "addition",
            "subtraction",
            "multiplication",
            "division"
        ],
        "tech_stack": [
            "HTML",
            "CSS",
            "JavaScript"
        ]
    }

    sample_architecture = {
        "files": [
            "index.html",
            "style.css",
            "script.js"
        ]
    }

    result = coder_agent(
        sample_plan,
        sample_architecture
    )

    print(result)
