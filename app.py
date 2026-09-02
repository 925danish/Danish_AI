import streamlit as st
from openai import OpenAI

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="Danish AI",
    page_icon="🤖",
    layout="centered"
)
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        opacity: 0.7;
        margin-bottom: 30px;
    }

    .stChatMessage {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# OpenAI connection
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Danish AI personality
# -----------------------------
SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

Normally:
- Answer questions clearly and helpfully.
- Be friendly and conversational.
- You can speak English or Urdu depending on the user's language.

Roast mode:
- If the user asks you to roast them, tease them, or says "roast me",
  give a funny playful roast.
- Keep roasts humorous and harmless.
- Never use hateful, threatening, or seriously abusive language.

You can switch naturally between helpful mode and playful roast mode.
"""

# -----------------------------
# Title
# -----------------------------
st.markdown('<div class="main-title">🤖 Danish AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Your AI assistant  🔥</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Ask Danish AI anything...")

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Danish AI is thinking... 🤔"):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Danish AI")

    st.write("### Features")
    st.write("💬 AI Chat")
    st.write("🇵🇰 Urdu + English")
    st.write("🔥 Roast Mode")
    st.write("🧠 Conversation Memory")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()
