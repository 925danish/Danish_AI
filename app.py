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
    initial_sidebar_state="expanded",
)

# ============================================================
# OPENAI
# ============================================================

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

SYSTEM_PROMPT = """
You are Danish AI, a professional, friendly and intelligent AI assistant.

Your job is to:
- Answer questions clearly.
- Help with programming and AI.
- Help users learn.
- Explain difficult topics simply.
- Be professional but friendly.
- Never pretend to be human.
"""

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False

# ============================================================
# STATISTICS
# ============================================================

def get_user_messages():
    return sum(
        1 for message in st.session_state.messages
        if message["role"] == "user"
    )


def get_ai_messages():
    return sum(
        1 for message in st.session_state.messages
        if message["role"] == "assistant"
    )


def get_total_messages():
    return len(st.session_state.messages)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

footer {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp {
    background:
        radial-gradient(
            circle at 75% 10%,
            rgba(102, 45, 255, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 20% 80%,
            rgba(40, 100, 255, 0.08),
            transparent 30%
        ),
        #070b1c;
    color: #ffffff;
}

.block-container {
    padding-top: 28px !important;
    padding-bottom: 30px !important;
    max-width: 1500px !important;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080d20 0%,
            #090d20 55%,
            #070b19 100%
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding: 20px 18px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 12px 8px 25px 8px;
}

.brand-logo {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    background: linear-gradient(135deg, #7c3cff, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow:
        0 8px 30px rgba(124,60,255,0.30),
        inset 0 1px rgba(255,255,255,0.20);
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.brand-subtitle {
    color: #8992b3;
    font-size: 11px;
    margin-top: 3px;
}

.sidebar-label {
    color: #69728f;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin: 18px 8px 10px 8px;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    height: 45px;
    border: 1px solid transparent;
    border-radius: 11px;
    background: transparent;
    color: #c7cce0;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(124,60,255,0.13);
    border-color: rgba(124,60,255,0.25);
    color: white;
}

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 20px 4px;
}

.premium {
    margin-top: 25px;
    padding: 18px;
    border-radius: 17px;
    background:
        linear-gradient(
            145deg,
            rgba(108, 42, 220, 0.27),
            rgba(49, 32, 112, 0.18)
        );
    border: 1px solid rgba(139,92,246,0.32);
    box-shadow: 0 15px 40px rgba(65,35,150,0.12);
}

.premium-title {
    font-size: 14px;
    font-weight: 800;
    color: #d8c7ff;
}

.premium-text {
    color: #8e95af;
    font-size: 12px;
    line-height: 1.6;
    margin: 8px 0 14px;
}

.premium-button {
    display: block;
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    background: linear-gradient(90deg, #743cff, #5924df);
    color: white;
    font-size: 12px;
    font-weight: 700;
}

.profile {
    border-top: 1px solid rgba(255,255,255,0.07);
    margin-top: 25px;
    padding: 18px 5px 5px;
    display: flex;
    align-items: center;
    gap: 11px;
}

.profile-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg,#7138ff,#4722bc);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}

.profile-name {
    color: white;
    font-size: 13px;
    font-weight: 700;
}

.profile-plan {
    color: #858da9;
    font-size: 11px;
    margin-top: 2px;
}

.page-title {
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #ffffff;
    margin-bottom: 5px;
}

.page-title span {
    color: #773cff;
}

.page-subtitle {
    color: #8d96b3;
    font-size: 13px;
}

.date-box {
    padding: 14px 18px;
    border-radius: 15px;
    background: rgba(22,27,49,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: left;
}

.date-main {
    font-size: 13px;
    font-weight: 700;
    color: white;
}

.date-time {
    color: #828aa5;
    font-size: 11px;
    margin-top: 4px;
}

.stat-card {
    min-height: 158px;
    padding: 20px;
    border-radius: 18px;
    background: rgba(17,22,43,0.82);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 15px 40px rgba(0,0,0,0.18);
    margin-bottom: 18px;
}

.stat-icon {
    width: 43px;
    height: 43px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 14px;
}

.purple-icon {
    background: rgba(137,53,255,0.17);
    border: 1px solid rgba(137,53,255,0.32);
}

.blue-icon {
    background: rgba(38,124,255,0.15);
    border: 1px solid rgba(38,124,255,0.28);
}

.green-icon {
    background: rgba(24,211,127,0.12);
    border: 1px solid rgba(24,211,127,0.25);
}

.orange-icon {
    background: rgba(255,158,32,0.12);
    border: 1px solid rgba(255,158,32,0.25);
}

.stat-number {
    font-size: 27px;
    font-weight: 800;
    color: white;
}

.stat-title {
    font-size: 13px;
    font-weight: 700;
    color: #b7bddd;
    margin-top: 2px;
}

.stat-description {
    color: #6f7896;
    font-size: 11px;
    margin-top: 4px;
}

.chat-panel {
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    background: rgba(9,14,32,0.72);
    overflow: hidden;
    margin-top: 8px;
}

.chat-header {
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-title {
    font-size: 19px;
    font-weight: 800;
    color: white;
}

.chat-subtitle {
    color: #7f88a6;
    font-size: 12px;
    margin-top: 4px;
}

.chat-icon {
    display: inline-flex;
    width: 38px;
    height: 38px;
    border-radius: 11px;
    background: linear-gradient(135deg,#773cff,#4f20c7);
    align-items: center;
    justify-content: center;
    margin-right: 10px;
}

.chat-message-user {
    background: linear-gradient(135deg,#7138ff,#5422cf);
    color: white;
    padding: 13px 17px;
    border-radius: 17px 17px 5px 17px;
    margin: 12px 0 12px auto;
    max-width: 75%;
    width: fit-content;
    font-size: 14px;
    box-shadow: 0 10px 25px rgba(94,40,220,0.22);
}

.chat-message-ai {
    background: #171d32;
    border: 1px solid rgba(255,255,255,0.08);
    color: #e0e4f0;
    padding: 13px 17px;
    border-radius: 17px 17px 17px 5px;
    margin: 12px auto 12px 0;
    max-width: 75%;
    width: fit-content;
    font-size: 14px;
}

.empty-chat {
    text-align: center;
    padding: 75px 20px;
}

.empty-icon {
    width: 70px;
    height: 70px;
    border-radius: 22px;
    background: linear-gradient(135deg,#7138ff,#4b27c8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    margin: 0 auto 18px;
    box-shadow: 0 15px 40px rgba(107,52,255,0.25);
}

.empty-title {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.empty-text {
    color: #7e87a5;
    font-size: 13px;
    margin-top: 7px;
}

.stChatInput {
    margin-top: 10px;
}

.stChatInput > div {
    background: #151b30 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 15px !important;
}

.stChatInput textarea {
    color: white !important;
}

.stChatInput textarea::placeholder {
    color: #68718e !important;
}

div[data-testid="stMetric"] {
    background: #11162b;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 15px;
}

.settings-card {
    background: #11162b;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 24px;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: #646d8b;
    font-size: 11px;
    margin-top: 35px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-logo">🤖</div>
            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-subtitle">Your intelligent AI Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    if st.button("🏠  Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("💬  AI Chat", use_container_width=True):
        st.session_state.page = "AI Chat"

    if st.button("📊  Usage & Stats", use_container_width=True):
        st.session_state.page = "Usage & Stats"

    if st.button("⚙️  Settings", use_container_width=True):
        st.session_state.page = "Settings"

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-label">CHAT</div>',
        unsafe_allow_html=True,
    )

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="premium">
            <div class="premium-title">👑 Danish AI Premium</div>
            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>
            <div class="premium-button">
                Upgrade Now
            </div>
        </div>

        <div class="profile">
            <div class="profile-circle">D</div>
            <div>
                <div class="profile-name">Danish</div>
                <div class="profile-plan">Free Plan</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# HEADER
# ============================================================

current_time = datetime.now()
date_text = current_time.strftime("%B %d, %Y")
time_text = current_time.strftime("%I:%M %p")

header_left, header_right = st.columns([5, 1])

with header_left:
    greeting = "Good morning"

    if current_time.hour >= 12 and current_time.hour < 18:
        greeting = "Good afternoon"
    elif current_time.hour >= 18:
        greeting = "Good evening"

    st.markdown(
        f"""
        <div class="page-title">
            {greeting}, <span>Danish</span> 👋
        </div>
        <div class="page-subtitle">
            Here's what's happening with Danish AI today.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        f"""
        <div class="date-box">
            <div class="date-main">📅 {date_text}</div>
            <div class="date-time">{time_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    total = get_total_messages()
    questions = get_user_messages()
    responses = get_ai_messages()
    roasts = sum(
        1
        for message in st.session_state.messages
        if message.get("roast", False)
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon purple-icon">💬</div>
                <div class="stat-number">{total}</div>
                <div class="stat-title">Messages</div>
                <div class="stat-description">Total messages</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon blue-icon">❓</div>
                <div class="stat-number">{questions}</div>
                <div class="stat-title">Questions</div>
                <div class="stat-description">Asked by you</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon green-icon">🤖</div>
                <div class="stat-number">{responses}</div>
                <div class="stat-title">AI Responses</div>
                <div class="stat-description">From Danish AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon orange-icon">🔥</div>
                <div class="stat-number">{roasts}</div>
                <div class="stat-title">Roast Mode</div>
                <div class="stat-description">Funny roasts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# AI CHAT
# ============================================================

if st.session_state.page in ["Dashboard", "AI Chat"]:

    st.markdown(
        """
        <div class="chat-panel">
            <div class="chat-header">
                <div>
                    <span class="chat-icon">💬</span>
                    <span class="chat-title">AI Chat</span>
                    <div class="chat-subtitle">
                        Talk with Danish AI.
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    if len(st.session_state.messages) == 0:

        st.markdown(
            """
            <div class="empty-chat">
                <div class="empty-icon">🤖</div>
                <div class="empty-title">How can I help you?</div>
                <div class="empty-text">
                    Ask Danish AI anything.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.markdown(
                    f"""
                    <div class="chat-message-user">
                        {message["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            elif message["role"] == "assistant":

                st.markdown(
                    f"""
                    <div class="chat-message-ai">
                        🤖 &nbsp; {message["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # ROAST MODE
    # ========================================================

    roast_col, empty_col = st.columns([1, 5])

    with roast_col:
        roast_clicked = st.button(
            "🔥 Roast Mode",
            use_container_width=True,
        )

        if roast_clicked:
            st.session_state.roast_mode = not st.session_state.roast_mode
            st.rerun()

    if st.session_state.roast_mode:
        st.info("🔥 Roast Mode is ON — Danish AI will answer with playful humor.")

    # ========================================================
    # CHAT INPUT
    # ========================================================

    prompt = st.chat_input("Type your message...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "roast": st.session_state.roast_mode,
            }
        )

        if client is None:

            answer = (
                "Your OpenAI API key is not connected. "
                "Please add OPENAI_API_KEY to Streamlit Secrets."
            )

        else:

            try:

                system_prompt = SYSTEM_PROMPT

                if st.session_state.roast_mode:
                    system_prompt += """
                    Roast Mode is enabled.
                    Give playful, harmless and funny responses.
                    Do not be hateful, threatening or abusive.
                    """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        }
                    ]
                    + [
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                        for message in st.session_state.messages
                    ],
                )

                answer = response.choices[0].message.content

            except Exception as error:

                answer = (
                    "Sorry, I couldn't connect to the AI right now.\n\n"
                    f"Error: {error}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "roast": st.session_state.roast_mode,
            }
        )

        st.rerun()

# ============================================================
# USAGE & STATS
# ============================================================

if st.session_state.page == "Usage & Stats":

    st.markdown(
        """
        <div class="page-title">
            Usage <span>&</span> Stats
        </div>
        <div class="page-subtitle">
            Your Danish AI activity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    total = get_total_messages()
    questions = get_user_messages()
    responses = get_ai_messages()

    a, b, c = st.columns(3)

    with a:
        st.metric("Total Messages", total)

    with b:
        st.metric("Questions", questions)

    with c:
        st.metric("AI Responses", responses)

    st.write("")

    st.markdown(
        """
        <div class="settings-card">
            <h3>📈 Activity Overview</h3>
            <p style="color:#7f88a6;">
                Your usage statistics will grow automatically as you chat
                with Danish AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SETTINGS
# ============================================================

if st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="page-title">
            Danish AI <span>Settings</span>
        </div>
        <div class="page-subtitle">
            Customize your assistant.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
        <div class="settings-card">
            <h3>🤖 Assistant</h3>
            <p style="color:#7f88a6;">
                Danish AI is your intelligent personal assistant.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.session_state.roast_mode = st.toggle(
        "🔥 Enable Roast Mode",
        value=st.session_state.roast_mode,
    )

    st.write("")

    if st.button("🗑️ Delete Conversation", use_container_width=True):
        st.session_state.messages = []
        st.success("Conversation cleared.")
        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Danish AI · Your Intelligent AI Assistant · Made with ❤️
    </div>
    """,
    unsafe_allow_html=True,
)
