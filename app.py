import streamlit as st
from openai import OpenAI
st.set_page_config(
   
    page_title="Danish AI |Your AI Assistant",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e1b4b 100%);
    color: white;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 5px;
    color: #ffffff;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #a5b4fc;
    margin-bottom: 35px;
}

/* Chat messages */
.stChatMessage {
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
}

/* Chat input */
.stChatInputContainer {
    border-radius: 18px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar heading */
[data-testid="stSidebar"] h2 {
    color: #a5b4fc;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(165,180,252,0.3);
    background: rgba(99,102,241,0.15);
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #818cf8;
    background: rgba(99,102,241,0.3);
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)




       
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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


st.markdown('<div class="main-title">🤖 Danish AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Your AI assistant  🔥</div>',
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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

   
    with st.chat_message("assistant"):
        with st.spinner("Danish AI is thinking... 🤔"):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


with st.sidebar:
    st.header("⚙️ Danish AI")

    st.write("### Features")
    st.write("💬 AI Chat")
    st.write("🇵🇰 Urdu + English")
    st.write("🧠 Conversation Memory")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()
