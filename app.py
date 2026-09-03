import streamlit as st
from openai import OpenAI
from datetime import datetime


# ============================================================
# PAGE SETTINGS
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

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# ============================================================
# AI PERSONALITY
# ============================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

You can:
- Answer general questions
- Help with Python and programming
- Help with AI and software engineering
- Help with business and freelancing
- Help with writing
- Speak English and Urdu

Always answer clearly and naturally.

ROAST MODE:
If the user asks "roast me", asks for a roast, or wants playful teasing:
- Give a funny and harmless roast.
- Keep it playful.
- Never use hateful, threatening, or seriously abusive language.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APP
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(91, 45, 180, 0.12),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 70%,
                rgba(37, 99, 235, 0.08),
                transparent 30%
            ),
            #080d20;

        color: #f8fafc;
    }


    /* ======================================================
       REMOVE STREAMLIT UI
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background: #080d20;
        border-right: 1px solid #202946;
    }

    [data-testid="stSidebar"] > div {
        padding: 22px 20px;
    }


    /* BRAND */

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 35px;
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        border-radius: 16px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 29px;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #4f46e5
            );

        box-shadow:
            0 8px 30px rgba(124, 58, 237, 0.35);
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
    }

    .brand-subtitle {
        color: #8993aa;
        font-size: 10px;
        margin-top: 3px;
    }


    /* SIDEBAR LABEL */

    .sidebar-title {
        color: #77829b;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-top: 20px;
        margin-bottom: 8px;
    }


    /* SIDEBAR BUTTONS */

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 43px;

        background: transparent;

        color: #dce2ef;

        border: 1px solid transparent;

        border-radius: 10px;

        text-align: left;

        font-size: 13px;

        font-weight: 500;

        margin-bottom: 5px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #1c1238;
        border-color: #51289a;
        color: #ffffff;
    }


    /* ======================================================
       PREMIUM
       ====================================================== */

    .premium-card {
        margin-top: 30px;

        padding: 17px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                #28134f,
                #15142e
            );

        border: 1px solid #57309b;
    }

    .premium-title {
        color: #c084fc;
        font-size: 14px;
        font-weight: 700;
    }

    .premium-text {
        color: #a6aec0;
        font-size: 11px;
        line-height: 1.5;
        margin-top: 7px;
        margin-bottom: 13px;
    }


    /* ======================================================
       PROFILE
       ====================================================== */

    .profile {
        border-top: 1px solid #202946;

        margin-top: 30px;
        padding-top: 18px;

        display: flex;
        align-items: center;
        gap: 10px;
    }

    .profile-icon {
        width: 40px;
        height: 40px;

        border-radius: 50%;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #38206c;

        color: #d8b4fe;

        font-weight: 800;
        font-size: 17px;
    }

    .profile-name {
        color: #ffffff;
        font-size: 13px;
        font-weight: 600;
    }

    .profile-plan {
        color: #7d879d;
        font-size: 10px;
        margin-top: 2px;
    }


    /* ======================================================
       MAIN HEADER
       ====================================================== */

    .heading {
        font-size: 35px;
        font-weight: 800;

        letter-spacing: -1.2px;

        color: #f8fafc;
    }

    .heading-purple {
        color: #8b5cf6;
    }

    .subtitle {
        color: #8792a9;
        font-size: 13px;
        margin-top:
