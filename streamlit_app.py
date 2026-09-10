import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.planner import planner_agent
from agents.architect import architect_agent
from agents.coder import coder_agent

st.set_page_config(page_title="AI Coding Assistant", layout="centered")

st.title("🤖 Multi-Agent Coding Assistant")

st.write("Enter your project idea and let AI generate a full project 🚀")

# 🧠 User Input
user_input = st.text_area("💡 Enter your project idea")

if st.button("Generate Project"):
    if user_input.strip() == "":
        st.warning("Please enter a project idea")
    else:
        with st.spinner("🧠 Planning..."):
            plan = planner_agent(user_input)
            st.subheader("🧠 Plan")
            st.json(plan)

        with st.spinner("🏗️ Designing Architecture..."):
            architecture = architect_agent(plan)
            st.subheader("🏗️ Architecture")
            st.json(architecture)

        with st.spinner("👨‍💻 Generating Code..."):
            result = coder_agent(plan, architecture)

        st.success("🎉 Project Generated Successfully!")
        st.write(result)