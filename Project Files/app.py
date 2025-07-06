import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="🧠 AI Dev Assistant", layout="wide")
st.title("🧠 Watsonx AI Dev Assistant")

st.sidebar.header("🔧 Tools")
mode = st.sidebar.radio("Choose a function:", [
    "Chat Assistant",
    "Generate Code",
    "Debug Code",
    "Compile Code",
    "Generate Requirements"
])

# ========== Shared Utility ==========
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}{endpoint}", json=payload)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

# ========== Mode Logic ==========

if mode == "Chat Assistant":
    st.subheader("🤖 Ask Anything")
    user_input = st.text_area("Your Message")
    if st.button("Chat"):
        if user_input.strip():
            result = call_api("/chat", {"message": user_input})
            st.success(result.get("response", result.get("error", "Error")))

elif mode == "Generate Code":
    st.subheader("🧪 Code Generator")
    prompt = st.text_area("Describe what you want to build")
    if st.button("Generate Code"):
        if prompt.strip():
            result = call_api("/generate-code", {"prompt": prompt})
            st.code(result.get("code", result.get("error", "Error")), language="python")

elif mode == "Debug Code":
    st.subheader("🐞 Code Debugger")
    code = st.text_area("Paste your buggy Python code")
    if st.button("Debug Code"):
        if code.strip():
            result = call_api("/debug-code", {"prompt": code})
            st.text_area("Debug Output", result.get("debugged_code", result.get("error", "Error")), height=300)

elif mode == "Compile Code":
    st.subheader("⚙️ Code Compiler (AI Output Simulator)")
    code = st.text_area("Paste code to simulate output")
    if st.button("Compile"):
        if code.strip():
            result = call_api("/compile-code", {"prompt": code})
            st.text_area("Output & Analysis", result.get("result", result.get("error", "Error")), height=300)

elif mode == "Generate Requirements":
    st.subheader("📋 Requirement Generator")
    description = st.text_area("Describe your project")
    if st.button("Generate Requirements"):
        if description.strip():
            result = call_api("/generate-requirements", {"prompt": description})
            st.text_area("Requirements", result.get("requirements", result.get("error", "Error")), height=300)

