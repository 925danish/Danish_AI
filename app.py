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
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

Your job is to:
- Answer questions clearly and helpfully.
- Help with coding, learning, writing, business and general questions.
- Speak English or Urdu depending on the user's language.
- Be friendly and conversational.

Roast Mode:
- If the user asks for a roast or says "roast me", give a funny,
  playful and harmless roast.
- Never use hateful, threatening or seriously abusive language.

Keep responses useful and natural.
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

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 25% 10%,
            rgba(79, 70, 229, 0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 70%,
            rgba(124, 58, 237, 0.08),
            transparent 30%
        ),
        #070b18;

    color: #f8fafc;
}


/* Hide Streamlit default branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background: #090e1d;
    border-right: 1px solid rgba(148,163,184,0.14);
}

[data-testid="stSidebar"] > div {
    padding: 24px 20px;
}


/* Brand */

.brand-box {
    padding: 4px 0 22px 0;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-logo {
    width: 45px;
    height: 45px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 25px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #4f46e5
        );

    box-shadow:
        0 8px 25px rgba(124,58,237,0.35);
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
}

.brand-description {
    color: #8b95aa;
    font-size: 11px;
    margin-top: 3px;
}


/* Navigation */

.section-label {
    color: #68738a;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin: 20px 0 9px 2px;
}


/* Sidebar buttons */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 42px;

    border-radius: 10px;

    border: 1px solid transparent;

    background: transparent;

    color: #d7dce8;

    text-align: left;

    font-weight: 500;
}


[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(124,58,237,0.14);
    border-color: rgba(124,58,237,0.20);
}


/* =====================================================
   PREMIUM CARD
   ===================================================== */

.premium-card {
    margin-top: 25px;

    padding: 18px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(124,58,237,0.24),
            rgba(79,70,229,0.08)
        );

    border: 1px solid rgba(139,92,246,0.28);
}

.premium-title {
    color: #c084fc;
    font-size: 14px;
    font-weight: 700;
}

.premium-text {
    color: #aab2c3;
    font-size: 11px;
    line-height: 1.5;
    margin: 8px 0 14px;
}


/* =====================================================
   PROFILE
   ===================================================== */

.profile-card {
    margin-top: 22px;
    padding-top: 18px;

    border-top: 1px solid rgba(148,163,184,0.12);
}

.profile-avatar {
    width: 38px;
    height: 38px;

    border-radius: 50%;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: 800;
    color: white;
}

.profile-name {
    font-size: 13px;
    font-weight: 600;
}

.profile-plan {
    color: #7f899d;
    font-size: 10px;
}


/* =====================================================
   MAIN HEADER
   ===================================================== */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.greeting {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}

.greeting-name {
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #a78bfa
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-subtitle {
    color: #8791a7;
    font-size: 14px;
    margin-top: 4px;
}


/* Date card */

.date-card {
    min-width: 155px;

    padding: 14px 18px;

    border-radius: 14px;

    background: rgba(15,23,42,0.8);

    border: 1px solid rgba(148,163,184,0.12);

    text-align: center;
}

.date-icon {
    font-size: 18px;
}

.date-text {
    font-size: 12px;
    color: #d9deea;
    font-weight: 600;
}


/* =====================================================
   STAT CARDS
   ===================================================== */

.stat-card {
    min-height: 160px;

    padding: 20px;

    border-radius: 17px;

    background: #0d1425;

    border: 1px solid rgba(148,163,184,0.13);

    position: relative;

    overflow: hidden;
}

.stat-card:hover {
    transform: translateY(-2px);
    transition: 0.2s;
}

.stat-purple {
    border-color: rgba(168,85,247,0.30);
}

.stat-blue {
    border-color: rgba(59,130,246,0.28);
}

.stat-green {
    border-color: rgba(34,197,94,0.25);
}

.stat-orange {
    border-color: rgba(245,158,11,0.27);
}

.stat-icon {
    width: 42px;
    height: 42px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 20px;

    margin-bottom: 16px;
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
    font-size: 28px;
    font-weight: 800;
}

.stat-title {
    font-size: 13px;
    font-weight: 600;
    margin-top: 2px;
}

.stat-description {
    color: #758096;
    font-size: 11px;
    margin-top: 5px;
}


/* =====================================================
   CHAT PANEL
   ===================================================== */

.chat-panel {
    margin-top: 25px;

    border-radius: 18px;

    background: #0b1120;

    border: 1px solid rgba(148,163,184,0.14);

    overflow: hidden;
}

.chat-header {
    padding: 20px 24px;

    border-bottom: 1px solid rgba(148,163,184,0.10);

    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-title {
    font-size: 20px;
    font-weight: 750;
}

.chat-subtitle {
    color: #7f899e;
    font-size: 12px;
    margin-top: 3px;
}


/* =====================================================
   CHAT MESSAGES
   ===================================================== */

.stChatMessage {
    border-radius: 15px;

    border: 1px solid rgba(148,163,184,0.10);

    background: rgba(255,255,255,0.025);

    margin-bottom: 10px;
}


/* =====================================================
   CHAT INPUT
   ===================================================== */

.stChatInputContainer {
    background: #111827;

    border: 1px solid rgba(129,140,248,0.30);

    border-radius: 16px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.22);
}


/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 10px;

    background: #111827;

    color: #e5e7eb;

    border: 1px solid rgba(148,163,184,0.15);

    font-weight: 600;
}

.stButton > button:hover {
    border-color: #7c3aed;

    background: rgba(124,58,237,0.15);
}


/* Purple buttons */

.purple-button .stButton > button {
    background: linear-gradient(
        135deg,
        #6d28d9,
        #7c3aed
    );

    border: none;

    color: white;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;

    color: #5f687c;

    font-size: 10px;

    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand-box">
        <div class="brand-row">
            <div class="brand-logo">🤖</div>

            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-description">
                    Your Intelligent AI Assistant
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="section-label">Workspace</div>',
        unsafe_allow_html=True
    )


    if st.button("🏠   Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()


    if st.button("💬   AI Chat"):
        st.session_state.page = "Chat"
        st.rerun()


    if st.button("📊   Usage & Stats"):
        st.session_state.page = "Stats"
        st.rerun()


    if st.button("⚙️   Settings"):
        st.session_state.page = "Settings"
        st.rerun()


    st.markdown(
        '<div class="section-label">Chat</div>',
        unsafe_allow_html=True
    )


    if st.button("🗑️   Clear Conversation"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()


    # Premium card

    st.markdown("""
    <div class="premium-card">
        <div class="premium-title">
            👑 Danish AI Premium
        </div>

        <div class="premium-text">
            Unlock more power and exclusive features.
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="purple-button">',
        unsafe_allow_html=True
    )

    if st.button("Upgrade Now"):
        st.info("Premium plans coming soon.")

    st.markdown("</div>", unsafe_allow_html=True)


    # Profile

    st.markdown("""
    <div class="profile-card">
        <div class="brand-row">
            <div class="profile-avatar">D</div>

            <div>
                <div class="profile-name">
                    Danish
                </div>

                <div class="profile-plan">
                    Free Plan
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    now = datetime.now()

    today = now.strftime("%B %d, %Y")
    current_time = now.strftime("%I:%M %p")


    # Header

    col1, col2 = st.columns([5, 1.2])

    with col1:

        st.markdown(
            """
            <div class="greeting">
                Good evening,
                <span class="greeting-name">
                    Danish
                </span>
                👋
            </div>

            <div class="header-subtitle">
                Here's what's happening with Danish AI today.
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="date-card">
                <div class="date-icon">📅</div>
                <div class="date-text">
                    {today}
                </div>
                <div class="date-text">
                    {current_time}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # STATS
    # =====================================================

    user_messages = [
        m for m in st.session_state.messages
        if m["role"] == "user"
    ]

    assistant_messages = [
        m for m in st.session_state.messages
        if m["role"] == "assistant"
    ]


    total_messages = (
        len(user_messages) +
        len(assistant_messages)
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
            <div class="stat-card stat-purple">

                <div class="stat-icon icon-purple">
                    💬
                </div>

                <div class="stat-number">
                    {total_messages}
                </div>

                <div class="stat-title">
                    Messages
                </div>

                <div class="stat-description">
                    Total messages
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="stat-card stat-blue">

                <div class="stat-icon icon-blue">
                    👤
                </div>

                <div class="stat-number">
                    {len(user_messages)}
                </div>

                <div class="stat-title">
                    Questions
                </div>

                <div class="stat-description">
                    Asked by you
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="stat-card stat-green">

                <div class="stat-icon icon-green">
                    🤖
                </div>

                <div class="stat-number">
                    {len(assistant_messages)}
                </div>

                <div class="stat-title">
                    AI Responses
                </div>

                <div class="stat-description">
                    From Danish AI
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            """
            <div class="stat-card stat-orange">

                <div class="stat-icon icon-orange">
                    🔥
                </div>

                <div class="stat-number">
                    0
                </div>

                <div class="stat-title">
                    Roast Mode
                </div>

                <div class="stat-description">
                    Funny roasts
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # CHAT PANEL HEADER
    # =====================================================

    st.markdown("""
    <div class="chat-panel">

        <div class="chat-header">

            <div>
                <div class="chat-title">
                    💬 AI Chat
                </div>

                <div class="chat-subtitle">
                    Talk with Danish AI.
                </div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    # New chat button

    new_chat_col, empty_col = st.columns([1, 5])

    with new_chat_col:

        if st.button("➕ New Chat"):

            st.session_state.messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            st.rerun()


    # =====================================================
    # CHAT
    # =====================================================

    if len(st.session_state.messages) == 1:

        st.markdown("""
        <div style="
            text-align:center;
            padding:45px 20px 25px;
        ">

            <div style="
                font-size:52px;
            ">
                🤖
            </div>

            <div style="
                font-size:30px;
                font-weight:800;
                margin-top:10px;
            ">
                How can I help you today?
            </div>

            <div style="
                color:#7f899e;
                font-size:13px;
                margin-top:8px;
            ">
                Ask me anything or start a conversation.
            </div>

        </div>
        """, unsafe_allow_html=True)


    else:

        for message in st.session_state.messages:

            if message["role"] == "system":
                continue

            with st.chat_message(message["role"]):

                st.markdown(message["content"])


    # =====================================================
    # CHAT INPUT
    # =====================================================

    user_input = st.chat_input(
        "Type your message..."
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

                    answer = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(answer)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )


                except Exception as e:

                    st.error(
                        "Something went wrong. Please try again."
                    )


# =========================================================
# AI CHAT PAGE
# =========================================================

elif st.session_state.page == "Chat":

    st.markdown(
        '<div class="greeting">AI Chat 💬</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-subtitle">Talk with Danish AI.</div>',
        unsafe_allow_html=True
    )


    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    user_input = st.chat_input(
        "Type your message..."
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


# =========================================================
# STATS PAGE
# =========================================================

elif st.session_state.page == "Stats":

    st.markdown(
        '<div class="greeting">Usage & Stats 📊</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-subtitle">Your Danish AI activity.</div>',
        unsafe_allow_html=True
    )


    user_count = len([
        m for m in st.session_state.messages
        if m["role"] == "user"
    ])

    ai_count = len([
        m for m in st.session_state.messages
        if m["role"] == "assistant"
    ])


    c1, c2, c3 = st.columns(3)


    with c1:
        st.metric(
            "Questions",
            user_count
        )


    with c2:
        st.metric(
            "AI Responses",
            ai_count
        )


    with c3:
        st.metric(
            "Total Messages",
            user_count + ai_count
        )


# =========================================================
# SETTINGS PAGE
# =========================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '<div class="greeting">Settings ⚙️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="header-subtitle">Customize Danish AI.</div>',
        unsafe_allow_html=True
    )


    st.markdown("### Preferences")


    language = st.selectbox(
        "Language",
        [
            "Automatic",
            "English",
            "Urdu"
        ]
    )


    theme = st.selectbox(
        "Theme",
        [
            "Danish Dark",
            "System"
        ]
    )


    st.markdown("### AI Features")


    roast = st.toggle(
        "🔥 Roast Mode",
        value=False
    )


    st.markdown("### About Danish AI")

    st.info(
        "Danish AI is your intelligent AI assistant."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Danish AI • Your Intelligent AI Assistant ♡
    </div>
    """,
    unsafe_allow_html=True
)
