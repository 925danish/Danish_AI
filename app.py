import streamlit as st
from openai import OpenAI

# ============================================================
# PAGE CONFIG
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
# SYSTEM PROMPTS
# ============================================================

NORMAL_PROMPT = (
    "You are Danish AI, a professional, friendly and intelligent AI assistant. "
    "Answer clearly and helpfully. You can communicate in English or Urdu. "
    "Keep answers natural, useful and easy to understand."
)

ROAST_PROMPT = (
    "You are Danish AI Roast Mode. Give funny, playful and harmless roasts. "
    "Never use hateful, threatening or seriously abusive language. "
    "Keep the roast entertaining."
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "AI Chat"

if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# ============================================================
# CUSTOM CSS
# ============================================================

css = "\n".join([
    "<style>",
    ".stApp {",
    "    background: #070b1c;",
    "    color: #f5f7ff;",
    "}",
    "[data-testid='stSidebar'] {",
    "    background: #0b1024;",
    "    border-right: 1px solid #20284a;",
    "}",
    "[data-testid='stSidebar'] * {",
    "    color: #e8ebff;",
    "}",
    ".brand {",
    "    font-size: 28px;",
    "    font-weight: 800;",
    "    color: #ffffff;",
    "    margin-bottom: 4px;",
    "}",
    ".brand span {",
    "    color: #8b5cf6;",
    "}",
    ".small-text {",
    "    color: #8d96b8;",
    "    font-size: 13px;",
    "}",
    ".hero {",
    "    background: linear-gradient(135deg, #111936, #171044);",
    "    border: 1px solid #29265c;",
    "    border-radius: 22px;",
    "    padding: 28px;",
    "    margin-bottom: 22px;",
    "}",
    ".hero-title {",
    "    font-size: 34px;",
    "    font-weight: 800;",
    "    margin: 0;",
    "}",
    ".hero-sub {",
    "    color: #9da6c7;",
    "    margin-top: 8px;",
    "}",
    ".stat-card {",
    "    background: #0d132b;",
    "    border: 1px solid #20284a;",
    "    border-radius: 18px;",
    "    padding: 20px;",
    "    min-height: 110px;",
    "}",
    ".stat-title {",
    "    color: #8f98ba;",
    "    font-size: 13px;",
    "}",
    ".stat-number {",
    "    font-size: 27px;",
    "    font-weight: 800;",
    "    margin-top: 8px;",
    "}",
    ".premium {",
    "    background: linear-gradient(135deg, #6d3df5, #8b5cf6);",
    "    border-radius: 18px;",
    "    padding: 18px;",
    "    margin-top: 25px;",
    "}",
    ".premium-title {",
    "    font-size: 18px;",
    "    font-weight: 800;",
    "}",
    ".chat-box {",
    "    background: #0d132b;",
    "    border: 1px solid #20284a;",
    "    border-radius: 20px;",
    "    padding: 20px;",
    "    margin-top: 15px;",
    "}",
    ".section-title {",
    "    font-size: 22px;",
    "    font-weight: 750;",
    "    margin-bottom: 12px;",
    "}",
    "div[data-testid='stChatMessage'] {",
    "    background: #0d132b;",
    "    border: 1px solid #20284a;",
    "    border-radius: 16px;",
    "    margin-bottom: 10px;",
    "}",
    "div[data-testid='stChatInput'] {",
    "    border-color: #393263;",
    "}",
    "</style>"
])

st.markdown(css, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<div class='brand'>Danish <span>AI</span> 🤖</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='small-text'>Your intelligent AI assistant</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Navigation")

    selected = st.radio(
        "Navigation",
        ["AI Chat", "Dashboard", "Roast Mode", "Settings"],
        label_visibility="collapsed"
    )

    st.session_state.mode = selected

    st.divider()

    st.markdown("### Quick Actions")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div class='premium'>"
        "<div class='premium-title'>⚡ Danish AI Pro</div>"
        "<div style='margin-top:6px;'>Unlock advanced AI features.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='small-text'>Danish AI v1.0</div>",
        unsafe_allow_html=True
    )

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.mode == "Dashboard":

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>Welcome to Danish AI 👋</div>"
        "<div class='hero-sub'>Your personal AI workspace.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-title'>Messages</div>"
            "<div class='stat-number'>" +
            str(st.session_state.total_messages) +
            "</div></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-title'>AI Mode</div>"
            "<div class='stat-number'>Active</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-title'>Languages</div>"
            "<div class='stat-number'>EN + UR</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-title'>Status</div>"
            "<div class='stat-number'>Online</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='chat-box'>"
        "<div class='section-title'>Danish AI Features</div>"
        "<div class='small-text'>"
        "💬 Intelligent AI Chat<br><br>"
        "🇵🇰 English + Urdu support<br><br>"
        "🔥 Playful Roast Mode<br><br>"
        "🧠 Conversation memory during the session"
        "</div></div>",
        unsafe_allow_html=True
    )

# ============================================================
# ROAST MODE
# ============================================================

elif st.session_state.mode == "Roast Mode":

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>🔥 Roast Mode</div>"
        "<div class='hero-sub'>"
        "Ready for a playful roast? Ask Danish AI."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.info("Try saying: Roast me 😂")

# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.mode == "Settings":

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>⚙️ Settings</div>"
        "<div class='hero-sub'>Customize your Danish AI experience.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.write("### AI Settings")

    language = st.selectbox(
        "Preferred response language",
        ["Automatic", "English", "Urdu"]
    )

    st.write("Selected language:", language)

    st.write("### About")

    st.info(
        "Danish AI is an AI assistant built with Python, "
        "Streamlit and OpenAI."
    )

# ============================================================
# AI CHAT
# ============================================================

else:

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>Danish AI 🤖</div>"
        "<div class='hero-sub'>"
        "Ask anything. Learn, create, solve and explore."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.messages:

        st.markdown(
            "<div class='chat-box'>"
            "<div class='section-title'>How can I help?</div>"
            "<div class='small-text'>"
            "Ask me anything about Python, AI, coding, business, "
            "learning or everyday questions."
            "</div></div>",
            unsafe_allow_html=True
        )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask Danish AI anything..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.total_messages += 1

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            if client is None:

                answer = (
                    "⚠️ OpenAI API key is not configured. "
                    "Please add OPENAI_API_KEY to Streamlit Secrets."
                )

                st.error(answer)

            else:

                try:

                    if st.session_state.mode == "Roast Mode":
                        system_prompt = ROAST_PROMPT
                    else:
                        system_prompt = NORMAL_PROMPT

                    api_messages = [
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ]

                    api_messages.extend(
                        st.session_state.messages
                    )

                    with st.spinner("Danish AI is thinking..."):

                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=api_messages
                        )

                    answer = response.choices[0].message.content

                    st.markdown(answer)

                except Exception as error:

                    answer = (
                        "⚠️ Something went wrong while contacting "
                        "the AI service.\n\n"
                        "Please check your OpenAI API key and try again."
                    )

                    st.error(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
