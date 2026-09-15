from langchain_openai import ChatOpenAI
import os
import json

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")


#  Initialize LLM (Groq)
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="openai/gpt-oss-20b",
    temperature=0
)
#  Planner Agent
def planner_agent(task: str):
    prompt = f"""
    You are a software planning assistant.


    Return ONLY valid JSON.
    Do NOT include markdown (no ```).


    JSON format:
    {{
        "project_name": "string",
        "features": ["feature1", "feature2"],
        "tech_stack": ["tech1", "tech2"]
    }}


    Request:
    {task}
    """


    response = llm.invoke(prompt).content


    #  Clean markdown if model still adds it
    cleaned = response.replace("```json", "").replace("```", "").strip()


    #  Convert to JSON
    try:
        data = json.loads(cleaned)
    except:
        print(" RAW RESPONSE:")
        print(response)
        data = {"error": "Invalid JSON output"}


    return data


#  Run test
if __name__ == "__main__":
    user_input = "Build a calculator web app with add, subtract, multiply and divide"


    result = planner_agent(user_input)


    print("\n Planner Output:")
    print(json.dumps(result, indent=4))

