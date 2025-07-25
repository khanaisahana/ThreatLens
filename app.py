
import os
import streamlit as st
from phishing_prompt import build_prompt
import requests
from dotenv import load_dotenv
load_dotenv()

st.sidebar.header("🔑 API Setup")
API_KEY = st.sidebar.text_input("Enter your OpenRouter API Key", type="password")
REFERER_URL = "https://sahanagenai.streamlit.app"  # Update this if your app URL changes

def call_openrouter(prompt):
    headers = {
    "Authorization": f"Bearer {API_KEY}",  # Replace API_KEY with your actual key
    "HTTP-Referer": "https://sahanakhanai-threatlens.streamlit.app/",  # Your deployed Streamlit app URL
    "Content-Type": "application/json"
   }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant for cybersecurity."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"] if res.status_code == 200 else res.text

# ==== Sidebar Navigation ====
st.sidebar.title("🔐 Threat Intelligence Assistant")
choice = st.sidebar.radio("Choose Tool", ["Phishing Analyzer", "Common Vulnerabilities and Exposures Explainer", "Log Summarizer"])

# ==== Phishing Analyzer ====
if choice == "Phishing Analyzer":
    st.title("🛡️ Phishing Email Analyzer")
    uploaded_file = st.file_uploader("Upload suspicious email (.txt)", type="txt")
    email_text = ""
    if uploaded_file:
        email_text = uploaded_file.read().decode("utf-8")
    else:
        email_text = st.text_area("Or paste the email content:", height=200)

    if st.button("Analyze"):
        prompt = build_prompt(email_text)
        with st.spinner("Analyzing using Mistral..."):
            result = call_openrouter(prompt)
            st.success("✅ Done")
            st.markdown(result)

# ==== CVE Explainer ====
elif choice == "Common Vulnerabilities and Exposures Explainer":
    st.title("🛡️ CVE Vulnerability Explainer")
    cve_id = st.text_input("Enter CVE ID (e.g., CVE-2023-12345)")
    if st.button("Explain CVE"):
        prompt = f"Explain {cve_id} in simple language. What is the risk, how is it exploited, and how can it be mitigated?"
        with st.spinner("Querying LLM..."):
            result = call_openrouter(prompt)
            st.success("✅ Done")
            st.markdown(result)

# ==== Log Summarizer ====
elif choice == "Log Summarizer":
    st.title("🛡️ Log File Summarizer")
    log_file = st.file_uploader("Upload a log file (.txt)", type="txt")
    if log_file:
        log_text = log_file.read().decode("utf-8")
        if st.button("Summarize Log"):
            prompt = f"Summarize the following security log and highlight any potential threats:\n\n{log_text}"
            with st.spinner("Analyzing..."):
                result = call_openrouter(prompt)
                st.success("✅ Done")
                st.markdown(result)
