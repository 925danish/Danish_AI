import streamlit as st
from openai import OpenAI

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Danish AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# OPENAI
# ============================================================

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "AI Chat"

if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# ============================================================
# PROMPTS
# ============================================================

NORMAL_PROMPT = (
    "You are Danish AI, a professional, friendly and intelligent AI assistant. "
    "Answer clearly and accurately. You can communicate in English or Urdu. "
    "Be conversational and helpful. "
)

ROAST_PROMPT = (
    "You are Danish AI Roast Mode. "
    "Give funny, playful and harmless roasts. "
    "Never use hateful, threatening or seriously abusive language. "
    "Keep the roast entertaining and friendly."
)

# ============================================================
# DESIGN
# ============================================================

css = "\n".join([
    "<style>",

    ".stApp {",
    "    background: #070914;",
    "    color: #f5f7ff;",
    "}",

    "[data-testid='stSidebar'] {",
    "    background: #090d1f;",
    "    border-right: 1px solid #202743;",
    "}",

    "[data-testid='stSidebar'] * {",
    "    color: #f3f4ff;",
    "}",

    ".brand {",
    "    font-size: 30px;",
    "    font-weight: 800;",
    "    letter-spacing: -1px;",
    "    margin-top: 8px;",
    "}",

    ".brand-ai {",
    "    color: #8b5cf6;",
    "}",

    ".tagline {",
    "    color: #7f89aa;",
    "    font-size: 13px;",
    "    margin-top: 5px;",
    "}",

    ".topbar {",
    "    display: flex;",
    "    justify-content: space-between;",
    "    align-items: center;",
    "    padding: 5px 0 20px 0;",
    "}",

    ".main-title {",
    "    font-size: 38px;",
    "    font-weight: 800;",
    "    letter-spacing: -1px;",
    "}",

    ".gradient-text {",
    "    background: linear-gradient(90deg, #8b5cf6, #4f8cff);",
    "    -webkit-background-clip: text;",
    "    -webkit-text-fill-color: transparent;",
    "}",

    ".subtitle {",
    "    color: #8e97b6;",
    "    font-size: 15px;",
    "    margin-top: 4px;",
    "}",

    ".hero {",
    "    background: linear-gradient(135deg, #101630, #17113b);",
    "    border: 1px solid #292d5b;",
    "    border-radius: 24px;",
    "    padding: 32px;",
    "    margin-bottom: 22px;",
    "    box-shadow: 0 15px 45px rgba(0,0,0,0.25);",
    "}",

    ".hero h2 {",
    "    margin: 0;",
    "    font-size: 31px;",
    "}",

    ".hero p {",
    "    color: #9aa4c6;",
    "    margin-top: 9px;",
    "}",

    ".card {",
    "    background: #0d1227;",
    "    border: 1px solid #202743;",
    "    border-radius: 20px;",
    "    padding: 22px;",
    "    min-height: 125px;",
    "}",

    ".card-label {",
    "    color: #858eae;",
    "    font-size: 13px;",
    "}",

    ".card-number {",
    "    font-size: 29px;",
    "    font-weight: 800;",
    "    margin-top: 9px;",
    "}",

    ".welcome-card {",
    "    background: #0d1227;",
    "    border: 1px solid #22294a;",
    "    border-radius: 22px;",
    "    padding: 28px;",
    "    margin-top: 18px;",
    "}",

    ".welcome-title {",
    "    font-size: 24px;",
    "    font-weight: 800;",
    "}",

    ".welcome-text {",
    "    color: #919abb;",
    "    margin-top: 8px;",
    "    line-height: 1.6;",
    "}",

    ".pro-card {",
    "    ba
