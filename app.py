import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

st.set_page_config(
    page_title="Danish_AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Danish_AI")
st.caption("Your personal AI assistant.")

st.info("👋 Hello! I am Danish_AI. Ask me anything!")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if st.button("🧹 Clear Chat"):
    st.session_state.conversation = []
    st.rerun()

for message in st.session_state.conversation:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])

    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message["content"])

message = st.chat_input("💬 Type your message...")

if message:

    st.session_state.conversation.append({
        "role": "user",
        "content": message
    })

    with st.chat_message("user"):
        st.write(message)

    with st.chat_message("assistant", avatar="🤖"):

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="""
You are Danish_AI, a friendly and funny AI assistant.

Your personality:
- Be friendly and helpful.
- Use simple language.
- Understand English, Urdu, and Roman Urdu.
- Be funny when appropriate.
- If the user asks for a roast, give a playful roast.
- Do not use hateful or harmful insults.
- Keep normal answers clear and useful.
""",
            input=st.session_state.conversation
        )

        answer = response.output_text

        st.write(answer)

    st.session_state.conversation.append({
        "role": "assistant",
        "content": answer
    })