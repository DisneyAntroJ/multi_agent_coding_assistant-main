from langchain_openai import ChatOpenAI
import os
import json


# 🔑 Set your Groq API key here
os.environ["GROQ_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = os.environ["GROQ_API_KEY"]


#  Initialize LLM (Groq)
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",
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

