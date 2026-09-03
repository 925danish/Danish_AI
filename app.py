import streamlit as st
from openai import OpenAI


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Danish AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# OPENAI
# ==================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

Answer questions clearly and helpfully.

You can communicate in English or Urdu depending on the user's language.

If the user asks to roast them:
- Give a funny playful roast.
- Keep it harmless.
- Never use hateful, threatening, or seriously abusive language.

Be conversational and helpful.
"""


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(99,102,241,0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(168,85,247,0.12),
            transparent 30%
        ),
        #080b16;
    color: #ffffff;
}


/* Remove Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background: #0b0f1c;
    border-right: 1px solid rgba(255,255,255,0.07);
}

[data-testid="stSidebar"] > div {
    padding-top: 25px;
}


/* Brand */

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 5px;
}

.brand-gradient {
    background: linear-gradient(
        90deg,
        #818cf8,
        #c084fc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    color: #7c849d;
    font-size: 12px;
    margin-bottom: 30px;
}


/* Navigation */

.nav-title {
    color: #667085;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}


/* Dashboard title */

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #8992aa;
    font-size: 16px;
    margin-bottom: 30px;
}


/* Cards */

.card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    min-height: 145px;
    box-shadow:
        0 15px 40px rgba(0,0,0,0.18);
}

.card:hover {
    border-color: rgba(129,140,248,0.35);
}

.card-icon {
    font-size: 28px;
    margin-bottom: 15px;
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 8px;
}

.card-text {
    color: #8992aa;
    font-size: 13px;
}


/* Stats */

.stat-card {
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.16),
        rgba(168,85,247,0.10)
    );

    border: 1px solid rgba(129,140,248,0.18);
    border-radius: 18px;
    padding: 20px;
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
}

.stat-label {
    color: #8992aa;
    font-size: 13px;
}


/* Chat */

.stChatMessage {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
}


/* Chat input */

.stChatInputContainer {
    background: #111625;
    border: 1px solid rgba(129,140,248,0.3);
    border-radius: 18px;
}


/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(129,140,248,0.2);
    background: rgba(255,255,255,0.04);
    color: white;
    font-weight: 600;
    padding: 10px;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    border-color: transparent;
}


/* Primary button */

.primary-button button {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    ) !important;

    border: none !important;
}


/* Divider */

.divider {
    height: 1px;
    background: rgba(255,255,255,0.07);
    margin: 25px 0;
}


/* Welcome */

.welcome {
    text-align: center;
    padding: 45px 20px 25px;
}

.welcome-icon {
    font-size: 55px;
}

.welcome-title {
    font-size: 34px;
    font-weight: 800;
    margin-top: 10px;
}

.welcome-text {
    color: #8992aa;
    font-size: 15px;
}


/* Footer */

.custom-footer {
    text-align: center;
    color: #555e75;
    font-size: 11px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            🤖 <span class="brand-gradient">Danish AI</span>
        </div>

        <div class="brand-subtitle">
            Your intelligent AI assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-title">Workspace</div>',
        unsafe_allow_html=True
    )

    if st.button("🏠  Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("💬  AI Chat"):
        st.session_state.page = "Chat"
        st.rerun()

    if st.button("📊  Usage & Stats"):
        st.session_state.page = "Stats"
        st.rerun()

    if st.button("⚙️  Settings"):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="nav-title">Chat</div>',
        unsafe_allow_html=True
    )

    if st.button("🗑️  Clear Conversation"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()

    st.markdown("---")

    st.caption("Danish AI")
    st.caption("© 2026 Danish AI")


# ==================================================
# DASHBOARD
# ==================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="dashboard-title">Welcome to Danish AI 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Your personal intelligent AI workspace.</div>',
        unsafe_allow_html=True
    )


    # Stats row

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">🤖</div>
                <div class="stat-label">AI Assistant</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {len(st.session_state.messages) - 1}
                </div>
                <div class="stat-label">Messages</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">EN / اردو</div>
                <div class="stat-label">Languages</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">🔥</div>
                <div class="stat-label">Roast Mode</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("### What can Danish AI do?")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">💬</div>
                <div class="card-title">AI Conversations</div>
                <div class="card-text">
                    Ask questions, brainstorm ideas,
                    learn new topics and get intelligent answers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🧠</div>
                <div class="card-title">Smart Assistance</div>
                <div class="card-text">
                    Get help with coding, writing,
                    learning, business and everyday tasks.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🇵🇰</div>
                <div class="card-title">English + Urdu</div>
                <div class="card-text">
                    Communicate naturally in English
                    or Urdu depending on your preference.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🚀</div>
                <div class="card-title">Ready to get started?</div>
                <div class="card-text">
                    Open AI Chat and start a conversation
                    with Danish AI.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">
                <div class="card-icon">✨</div>
                <div class="card-title">Built for Danish AI</div>
                <div class="card-text">
                    A custom AI experience with its own
                    visual identity and dashboard.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# CHAT
# ==================================================

elif st.session_state.page == "Chat":

    st.markdown(
        '<div class="dashboard-title">AI Chat 💬</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Talk with Danish AI.</div>',
        unsafe_allow_html=True
    )


    # Welcome message when chat is empty

    if len(st.session_state.messages) == 1:

        st.markdown(
            """
            <div class="welcome">
                <div class="welcome-icon">🤖</div>
                <div class="welcome-title">
                    How can I help you?
                </div>
                <div class="welcome-text">
                    Ask Danish AI anything.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Display messages

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Chat input

    user_input = st.chat_input(
        "Message Danish AI..."
    )


    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)


        with st.chat_message("assistant"):

            with st.spinner("Danish AI is thinking..."):

                try:

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

                except Exception:

                    st.error(
                        "Sorry, something went wrong. Please try again."
                    )


# ==================================================
# STATS
# ==================================================

elif st.session_state.page == "Stats":

    st.markdown(
        '<div class="dashboard-title">Usage & Stats 📊</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Your Danish AI activity.</div>',
        unsafe_allow_html=True
    )


    user_messages = [
        m for m in st.session_state.messages
        if m["role"] == "user"
    ]

    assistant_messages = [
        m for m in st.session_state.messages
        if m["role"] == "assistant"
    ]


    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {len(user_messages)}
                </div>
                <div class="stat-label">
                    Questions Asked
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">
                    {len(assistant_messages)}
                </div>
                <div class="stat-label">
                    AI Responses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">
                    Active
                </div>
                <div class="stat-label">
                    AI Status
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# SETTINGS
# ==================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '<div class="dashboard-title">Settings ⚙️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Customize your Danish AI experience.</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🤖</div>
            <div class="card-title">Danish AI</div>
            <div class="card-text">
                Personal AI assistant powered by OpenAI.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<br>", unsafe_allow_html=True)

    st.write("### Language")

    st.selectbox(
        "Preferred language",
        ["Automatic", "English", "Urdu"]
    )

    st.write("### Appearance")

    st.selectbox(
        "Theme",
        ["Danish Dark", "System"]
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="custom-footer">
        Danish AI • Your Intelligent AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)
