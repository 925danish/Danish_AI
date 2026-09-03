import streamlit as st
from openai import OpenAI
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Danish AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# OPENAI
# =========================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================================================
# AI INSTRUCTIONS
# =========================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

Rules:
- Answer questions clearly and helpfully.
- Help with coding, learning, writing, business and general questions.
- Speak English or Urdu depending on the user's language.
- Be friendly and conversational.

If the user says "roast me" or asks for a roast:
- Give a funny, playful and harmless roast.
- Never use hateful, threatening or seriously abusive language.
"""


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

/* ===============================
   APP
   =============================== */

.stApp {
    background: #080c18;
    color: #ffffff;
}


/* Remove default Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ===============================
   SIDEBAR
   =============================== */

[data-testid="stSidebar"] {
    background: #090e1b;
    border-right: 1px solid #20283a;
}

[data-testid="stSidebar"] > div {
    padding: 25px 20px;
}


/* Sidebar logo */

.logo {
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 3px;
}

.logo span {
    color: #8b5cf6;
}

.logo-sub {
    color: #7f8aa3;
    font-size: 11px;
    margin-bottom: 28px;
}


/* Sidebar section */

.sidebar-label {
    color: #69758d;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-top: 22px;
    margin-bottom
