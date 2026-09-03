import streamlit as st
from openai import OpenAI
from datetime import datetime


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

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Danish AI, a professional, friendly and intelligent AI assistant.

Your responsibilities:
- Answer questions clearly and accurately.
- Be helpful, friendly and conversational.
- You can communicate in English or Urdu.
- If the user writes Urdu, respond naturally in Urdu.
- If the user writes English, respond in English.
- Keep answers easy to understand unless the user asks for detailed information.

Roast Mode:
- If the user asks for a roast or says "roast me", give a funny playful roast.
- Keep it harmless and humorous.
- Never use hateful, threatening or seriously abusive language.
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

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "responses" not in st.session_state:
    st.session_state.responses = 0

if "roasts" not in st.session_state:
    st.session_state.roasts = 0

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    '''
    <style>

    /* =========================
       REMOVE STREAMLIT BRANDING
       ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    [data-testid="stDecoration"] {
        display: none;
    }


    /* =========================
       MAIN APP
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 75% 10%,
                rgba(105, 45, 255, 0.16),
                transparent 35%
            ),
            radial-gradient(
                circle at 30% 80%,
                rgba(40, 100, 255, 0.10),
                transparent 35%
            ),
            #070b1d;
        color: #f5f7ff;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1500px;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #080c20 0%,
                #0b1028 55%,
                #080c1c 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    /* =========================
       BRAND
       ========================= */

    .brand {
        padding: 10px 8px 25px 8px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        background:
            linear-gradient(
                135deg,
                #8b35ff,
                #4b20d6
            );
        box-shadow:
            0 0 30px rgba(126, 55, 255, 0.35);
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        color: white;
    }

    .brand-subtitle {
        color: #8e98b8;
        font-size: 12px;
        margin-top: 2px;
    }


    /* =========================
       SIDEBAR SECTION
       ========================= */

    .sidebar-label {
        color: #7e88a8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 18px;
        margin-bottom: 10px;
    }


    /* =========================
       SIDEBAR BUTTONS
       ========================= */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 45px;
        text-align: left;
        border-radius: 12px;
        border: 1px solid transparent;
        background: transparent;
        color: #dce1f4;
        font-size: 14px;
        font-weight: 600;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(116, 52, 255, 0.15);
        border-color: rgba(135, 78, 255, 0.3);
        color: white;
    }


    /* =========================
       PREMIUM CARD
       ========================= */

    .premium-card {
        margin-top: 28px;
        padding: 18px;
        border-radius: 16px;
        background:
            linear-gradient(
                135deg,
                rgba(115, 39, 255, 0.28),
                rgba(70, 26, 150, 0.12)
            );
        border: 1px solid rgba(141, 82, 255, 0.35);
    }

    .premium-title {
        font-size: 15px;
        font-weight: 700;
        color: white;
    }

    .premium-text {
        color: #a8afd0;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 7px;
        margin-bottom: 14px;
    }


    /* =========================
       USER CARD
       ========================= */

    .user-card {
        margin-top: 25px;
        padding: 15px 5px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    .user-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg,#812cff,#4520c5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
        float: left;
        margin-right: 10px;
    }

    .user-name {
        font-size: 14px;
        font-weight: 700;
        color: white;
    }

    .user-plan {
        color: #8d96b6;
        font-size: 11px;
    }


    /* =========================
       TOP HEADER
       ========================= */

    .welcome {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 3px;
        color: white;
    }

    .welcome-name {
        color: #7d3cff;
        text-shadow: 0 0 25px rgba(125,60,255,0.35);
    }

    .welcome-sub {
        color: #8993b4;
        font-size: 14px;
    }


    /* =========================
       DATE CARD
       ========================= */

    .date-card {
        background: rgba(23, 28, 53, 0.75);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 15px 20px;
        text-align: center;
        color: #e8ebf8;
    }


    /* =========================
       STAT CARDS
       ========================= */

    .stat-card {
        min-height: 190px;
        padding: 22px;
        border-radius: 20px;
        background: rgba(17, 22, 45, 0.85);
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }

    .stat-purple {
        border-color: rgba(151,70,255,0.40);
        box-shadow: inset 0 0 40px rgba(126,42,255,0.07);
    }

    .stat-blue {
        border-color: rgba(44,137,255,0.38);
        box-shadow: inset 0 0 40px rgba(30,120,255,0.06);
    }

    .stat-green {
        border-color: rgba(28,220,139,0.30);
        box-shadow: inset 0 0 40px rgba(20,220,120,0.05);
    }

    .stat-orange {
        border-color: rgba(255,165,38,0.32);
        box-shadow: inset 0 0 40px rgba(255,165,38,0.05);
    }

    .stat-icon {
        font-size: 25px;
        margin-bottom: 15px;
    }

    .stat-number {
        font-size: 31px;
        font-weight: 800;
        color: white;
    }

    .stat-title {
        font-size: 15px;
        font-weight: 700;
        margin-top: 5px;
        color: #c8cdf0;
    }

    .stat-description {
        font-size: 12px;
        color: #7f89aa;
        margin-top: 4px;
    }


    /* =========================
       CHAT PANEL
       ========================= */

    .chat-panel {
        margin-top: 25px;
        padding: 25px;
        border-radius: 22px;
        background: rgba(9, 14, 34, 0.88);
        border: 1px solid rgba(255,255,255,0.09);
        min-height: 480px;
    }

    .chat-title {
        font-size: 24px;
        font-weight: 800;
        color: white;
    }

    .chat-subtitle {
        color: #8993b4;
        font-size: 13px;
    }


    /* =========================
       CHAT MESSAGES
       ========================= */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        margin-top: 10px;
    }

    [data-testid="stChatInput"] textarea {
        background: #171d36 !important;
        color: white !important;
        border: 1px solid #30395d !important;
        border-radius: 16px !important;
    }


    /* =========================
       NORMAL BUTTONS
       ========================= */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(130,70,255,0.35);
        background: rgba(91,42,190,0.18);
        color: #eeeaff;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #8c4dff;
        background: rgba(112,53,240,0.30);
        color: white;
    }


    /* =========================
       FOOTER
       ========================= */

    .custom-footer {
        text-align: center;
        color: #737c9d;
        font-size: 12px;
        padding: 30px;
    }

    .heart {
        color: #a44cff;
    }

    </style>
    ''',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '''
        <div class="brand">
            <div class="brand-row">
                <div class="brand-icon">🤖</div>
                <div>
                    <div class="brand-name">Danish AI</div>
                    <div class="brand-subtitle">
                        Your intelligent AI Assistant
                    </div>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    if st.button("🏠  Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("💬  AI Chat", use_container_width=True):
        st.session_state.page = "AI Chat"
        st.rerun()

    if st.button("📊  Usage & Stats", use_container_width=True):
        st.session_state.page = "Usage & Stats"
        st.rerun()

    if st.button("⚙️  Settings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown(
        '<div class="sidebar-label">CHAT</div>',
        unsafe_allow_html=True
    )

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.session_state.questions = 0
        st.session_state.responses = 0
        st.session_state.roasts = 0

        st.rerun()

    st.markdown(
        '''
        <div class="premium-card">
            <div class="premium-title">👑 Danish AI Premium</div>
            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '''
        <div class="user-card">
            <div class="user-avatar">D</div>
            <div class="user-name">Danish</div>
            <div class="user-plan">Free Plan</div>
        </div>
        ''',
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

current_date = datetime.now().strftime("%B %d, %Y")
current_time = datetime.now().strftime("%I:%M %p")


col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '''
        <div class="welcome">
            Good evening,
            <span class="welcome-name">Danish</span> 👋
        </div>

        <div class="welcome-sub">
            Here's what's happening with Danish AI today.
        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f'''
        <div class="date-card">
            📅<br>
            <b>{current_date}</b><br>
            <small>{current_time}</small>
        </div>
        ''',
        unsafe_allow_html=True
    )


# ============================================================
# STATISTICS
# ============================================================

total_messages = (
    len(st.session_state.messages) - 1
)

questions = st.session_state.questions
responses = st.session_state.responses
roasts = st.session_state.roasts


s1, s2, s3, s4 = st.columns(4)


with s1:

    st.markdown(
        f'''
        <div class="stat-card stat-purple">
            <div class="stat-icon">💬</div>
            <div class="stat-number">{total_messages}</div>
            <div class="stat-title">Messages</div>
            <div class="stat-description">
                Total messages
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with s2:

    st.markdown(
        f'''
        <div class="stat-card stat-blue">
            <div class="stat-icon">❓</div>
            <div class="stat-number">{questions}</div>
            <div class="stat-title">Questions</div>
            <div class="stat-description">
                Asked by you
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with s3:

    st.markdown(
        f'''
        <div class="stat-card stat-green">
            <div class="stat-icon">🤖</div>
            <div class="stat-number">{responses}</div>
            <div class="stat-title">AI Responses</div>
            <div class="stat-description">
                From Danish AI
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


with s4:

    st.markdown(
        f'''
        <div class="stat-card stat-orange">
            <div class="stat-icon">🔥</div>
            <div class="stat-number">{roasts}</div>
            <div class="stat-title">Roast Mode</div>
            <div class="stat-description">
                Funny roasts
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


# ============================================================
# PAGE: DASHBOARD / CHAT
# ============================================================

if st.session_state.page in ["Dashboard", "AI Chat"]:

    st.markdown(
        '''
        <div class="chat-panel">
            <div class="chat-title">💬 AI Chat</div>
            <div class="chat-subtitle">
                Talk with Danish AI.
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Roast mode button
    roast_col, empty_col = st.columns([1, 5])

    with roast_col:

        roast_text = (
            "🔥 Roast Mode ON"
            if st.session_state.roast_mode
            else "🔥 Roast Mode"
        )

        if st.button(roast_text, use_container_width=True):
            st.session_state.roast_mode = not st.session_state.roast_mode
            st.rerun()


    # Show conversation
    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # Chat input
    user_input = st.chat_input(
        "Type your message..."
    )


    if user_input:

        # Count question
        st.session_state.questions += 1

        # Roast mode prompt
        actual_prompt = user_input

        if st.session_state.roast_mode:

            actual_prompt = (
                "Roast the user in a funny and harmless way. "
                "User message: " + user_input
            )

            st.session_state.roasts += 1


        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": actual_prompt
            }
        )


        with st.chat_message("user"):

            st.markdown(user_input)


        # Ask AI
        with st.chat_message("assistant"):

            with st.spinner("Danish AI is thinking..."):

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )

                    answer = response.choices[0].message.content

                except Exception as e:

                    answer = (
                        "Sorry, something went wrong while "
                        "connecting to Danish AI.\n\n"
                        f"Error: {e}"
                    )

                st.markdown(answer)


        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.session_state.responses += 1

        st.rerun()


# ============================================================
# PAGE: USAGE & STATS
# ============================================================

elif st.session_state.page == "Usage & Stats":

    st.subheader("📊 Usage & Stats")

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Questions",
            st.session_state.questions
        )

    with b:
        st.metric(
            "AI Responses",
            st.session_state.responses
        )

    with c:
        st.metric(
            "Roasts",
            st.session_state.roasts
        )

    st.markdown("---")

    st.write("### Conversation Information")

    st.write(
        f"Total messages: {total_messages}"
    )

    st.write(
        "Danish AI is ready to assist you in "
        "English and Urdu."
    )


# ============================================================
# PAGE: SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    st.subheader("⚙️ Settings")

    st.write("### Danish AI")

    st.write(
        "Your personal AI assistant."
    )

    st.checkbox(
        "Enable Roast Mode",
        value=st.session_state.roast_mode,
        key="settings_roast"
    )

    if st.button("Save Settings"):

        st.session_state.roast_mode = (
            st.session_state.settings_roast
        )

        st.success("Settings saved successfully!")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '''
    <div class="custom-footer">
        Danish AI • Your Intelligent AI Assistant
        <span class="heart">♡</span>
    </div>
    ''',
    unsafe_allow_html=True
)
