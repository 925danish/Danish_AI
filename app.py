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
    initial_sidebar_state="expanded",
)


# =========================================================
# OPENAI
# =========================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly, intelligent and helpful AI assistant.

Rules:
- Answer clearly and accurately.
- Be friendly and conversational.
- Speak English or Urdu depending on the user's language.
- Help with coding, AI, business, education and general questions.
- If the user asks for a roast, provide a funny harmless playful roast.
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

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 10%, rgba(108, 55, 255, 0.16), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(35, 105, 255, 0.10), transparent 25%),
        #070b1b;
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1500px;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #080c20 0%,
        #090d22 55%,
        #080b19 100%
    );
    border-right: 1px solid rgba(255,255,255,0.10);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}


/* BRAND */

.brand {
    padding: 10px 10px 28px 10px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-logo {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    background: linear-gradient(135deg, #7c3cff, #4f46e5);
    box-shadow: 0 0 30px rgba(124,60,255,0.35);
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

.brand-subtitle {
    font-size: 12px;
    color: #8e96b5;
    margin-top: 3px;
}


/* SIDEBAR SECTION */

.side-title {
    color: #6f7898;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.4px;
    margin: 20px 10px 10px 10px;
}


/* BUTTONS */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: transparent;
    color: #dfe3f4;
    text-align: left;
    font-weight: 600;
    min-height: 44px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: rgba(124,60,255,0.7);
    background: rgba(124,60,255,0.12);
    color: white;
}


/* PREMIUM CARD */

.premium-card {
    margin-top: 25px;
    padding: 18px;
    border-radius: 17px;
    background:
        linear-gradient(
            145deg,
            rgba(124,60,255,0.28),
            rgba(56,35,125,0.12)
        );
    border: 1px solid rgba(132,82,255,0.35);
    box-shadow: 0 10px 40px rgba(0,0,0,0.20);
}

.premium-title {
    color: #d4b8ff;
    font-size: 14px;
    font-weight: 800;
}

.premium-text {
    color: #aeb5d0;
    font-size: 12px;
    line-height: 1.5;
    margin: 8px 0 14px 0;
}


/* PROFILE */

.profile-card {
    margin-top: 25px;
    padding: 14px;
    border-top: 1px solid rgba(255,255,255,0.08);
}

.profile-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3cff, #5427c7);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}

.profile-name {
    font-weight: 700;
    color: white;
}

.profile-plan {
    font-size: 11px;
    color: #858dab;
}


/* HEADER */

.welcome-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.2px;
    margin-bottom: 5px;
}

.gradient-text {
    background: linear-gradient(90deg, #8b5cf6, #5b7cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.welcome-subtitle {
    color: #858dab;
    font-size: 15px;
    margin-bottom: 25px;
}


/* DATE CARD */

.date-card {
    background: rgba(22,27,49,0.72);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 15px 20px;
    text-align: center;
}

.date-label {
    color: #8d95b0;
    font-size: 11px;
}

.date-value {
    color: white;
    font-size: 14px;
    font-weight: 700;
}


/* STAT CARDS */

.stat-card {
    min-height: 190px;
    padding: 20px;
    border-radius: 20px;
    background: rgba(16,21,42,0.82);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 15px 45px rgba(0,0,0,0.18);
}

.stat-purple {
    border-color: rgba(168,85,247,0.35);
}

.stat-blue {
    border-color: rgba(59,130,246,0.35);
}

.stat-green {
    border-color: rgba(34,197,94,0.30);
}

.stat-orange {
    border-color: rgba(245,158,11,0.30);
}

.stat-icon {
    width: 45px;
    height: 45px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 18px;
}

.icon-purple {
    background: rgba(168,85,247,0.15);
}

.icon-blue {
    background: rgba(59,130,246,0.15);
}

.icon-green {
    background: rgba(34,197,94,0.13);
}

.icon-orange {
    background: rgba(245,158,11,0.13);
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: white;
}

.stat-name {
    font-size: 14px;
    font-weight: 700;
    margin-top: 4px;
}

.stat-desc {
    color: #737c9d;
    font-size: 12px;
    margin-top: 5px;
}


/* CHAT PANEL */

.chat-panel {
    margin-top: 32px;
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    background: rgba(8,12,30,0.60);
    box-shadow: 0 20px 70px rgba(0,0,0,0.18);
    padding: 25px;
}

.chat-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

.chat-subtitle {
    color: #7e87a5;
    font-size: 13px;
}


/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.07);
    background: rgba(22,28,50,0.72);
    padding: 12px;
    margin-bottom: 12px;
}


/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: transparent;
}

[data-testid="stChatInput"] > div {
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    background: #171d32 !important;
}


/* DIVIDER */

.divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 22px 0;
}


/* FOOTER */

.custom-footer {
    text-align: center;
    color: #68718f;
    font-size: 12px;
    margin-top: 25px;
    padding-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-row">
            <div class="brand-logo">🤖</div>
            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-subtitle">Your intelligent AI Assistant</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-title">WORKSPACE</div>', unsafe_allow_html=True)

    if st.button("⌂  Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("▣  AI Chat"):
        st.session_state.page = "AI Chat"
        st.rerun()

    if st.button("▥  Usage & Stats"):
        st.session_state.page = "Usage"
        st.rerun()

    if st.button("⚙  Settings"):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown('<div class="side-title">CHAT</div>', unsafe_allow_html=True)

    if st.button("🗑  Clear Conversation"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()

    st.markdown("""
    <div class="premium-card">
        <div class="premium-title">♛ Danish AI Premium</div>
        <div class="premium-text">
            Unlock more power and exclusive features.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="profile-card">
        <div class="brand-row">
            <div class="profile-avatar">D</div>
            <div>
                <div class="profile-name">Danish</div>
                <div class="profile-plan">Free Plan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# COUNTERS
# =========================================================

user_messages = sum(
    1 for m in st.session_state.messages
    if m["role"] == "user"
)

assistant_messages = sum(
    1 for m in st.session_state.messages
    if m["role"] == "assistant"
)

total_messages = user_messages + assistant_messages


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    now = datetime.now()

    if now.hour < 12:
        greeting = "Good morning"
    elif now.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            f"""
            <div class="welcome-title">
                {greeting}, <span class="gradient-text">Danish</span> 👋
            </div>
            <div class="welcome-subtitle">
                Here's what's happening with Danish AI today.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="date-card">
                <div class="date-label">TODAY</div>
                <div class="date-value">{now.strftime("%b %d, %Y")}</div>
                <div class="date-label">{now.strftime("%I:%M %p")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Stats
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="stat-card stat-purple">
                <div class="stat-icon icon-purple">💬</div>
                <div class="stat-number">{total_messages}</div>
                <div class="stat-name">Messages</div>
                <div class="stat-desc">Total messages</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat-card stat-blue">
                <div class="stat-icon icon-blue">♙</div>
                <div class="stat-number">{user_messages}</div>
                <div class="stat-name">Questions</div>
                <div class="stat-desc">Asked by you</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat-card stat-green">
                <div class="stat-icon icon-green">🤖</div>
                <div class="stat-number">{assistant_messages}</div>
                <div class="stat-name">AI Responses</div>
                <div class="stat-desc">From Danish AI</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="stat-card stat-orange">
                <div class="stat-icon icon-orange">🔥</div>
                <div class="stat-number">
                    {"ON" if st.session_state.roast_mode else "0"}
                </div>
                <div class="stat-name">Roast Mode</div>
                <div class="stat-desc">
                    {"Active" if st.session_state.roast_mode else "Funny roasts"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Chat section
    st.markdown("""
    <div class="chat-panel">
        <div class="chat-title">💬 AI Chat</div>
        <div class="chat-subtitle">Talk with Danish AI.</div>
    </div>
    """, unsafe_allow_html=True)

    # Show recent conversation
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Roast mode
    roast_col, new_col = st.columns([1, 5])

    with roast_col:
        if st.button(
            "🔥 Roast Mode" if not st.session_state.roast_mode
            else "🔥 Roast ON"
        ):
            st.session_state.roast_mode = not st.session_state.roast_mode
            st.rerun()

    with new_col:
        if st.button("＋ New Chat"):
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
            st.session_state.roast_mode = False
            st.rerun()


# =========================================================
# AI CHAT PAGE
# =========================================================

elif st.session_state.page == "AI Chat":

    st.markdown(
        '<div class="welcome-title">AI <span class="gradient-text">Chat</span> 💬</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">Talk with Danish AI.</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:

        if st.session_state.roast_mode:
            actual_input = (
                "Roast the user playfully and harmlessly. "
                "Keep it funny. User says: " + user_input
            )
        else:
            actual_input = user_input

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

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ] + [
                        {
                            "role": m["role"],
                            "content": (
                                actual_input
                                if m is st.session_state.messages[-1]
                                else m["content"]
                            )
                        }
                        for m in st.session_state.messages
                        if m["role"] != "system"
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()


# =========================================================
# USAGE PAGE
# =========================================================

elif st.session_state.page == "Usage":

    st.markdown(
        '<div class="welcome-title">Usage <span class="gradient-text">& Stats</span> 📊</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">Your Danish AI activity.</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.metric("Messages", total_messages)

    with b:
        st.metric("Questions", user_messages)

    with c:
        st.metric("AI Responses", assistant_messages)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.info(
        "Usage statistics are currently stored for this session. "
        "Persistent analytics can be added later."
    )


# =========================================================
# SETTINGS PAGE
# =========================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '<div class="welcome-title">Danish AI <span class="gradient-text">Settings</span> ⚙</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">Customize your assistant.</div>',
        unsafe_allow_html=True
    )

    st.checkbox("Enable Roast Mode", key="roast_mode")

    st.selectbox(
        "Preferred language",
        ["Auto", "English", "Urdu"]
    )

    st.selectbox(
        "AI Model",
        ["GPT-4o Mini"]
    )

    st.success("Settings are ready.")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="custom-footer">
        Danish AI • Your Intelligent AI Assistant • Made with ❤️
    </div>
    """,
    unsafe_allow_html=True
)
