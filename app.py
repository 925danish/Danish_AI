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

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are Danish AI, a friendly, intelligent and professional AI assistant.

Rules:
- Answer clearly and helpfully.
- You can communicate in English or Urdu.
- Match the user's language.
- Be conversational and professional.
- If the user asks for a roast, give a funny playful harmless roast.
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

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False

# ============================================================
# STATISTICS
# ============================================================

user_messages = [
    m for m in st.session_state.messages
    if m["role"] == "user"
]

assistant_messages = [
    m for m in st.session_state.messages
    if m["role"] == "assistant"
]

total_messages = len(user_messages) + len(assistant_messages)
questions = len(user_messages)
ai_responses = len(assistant_messages)

roast_count = 0

for message in user_messages:
    text = message["content"].lower()

    if (
        "roast me" in text
        or "roast me" in text
        or "roast" == text.strip()
    ):
        roast_count += 1

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 75% 10%, rgba(100, 45, 255, 0.12), transparent 28%),
        radial-gradient(circle at 25% 80%, rgba(20, 90, 255, 0.08), transparent 30%),
        #070b1c;
    color: #f5f7ff;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

/* Remove default top spacing */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080c20 0%,
            #090d22 50%,
            #070a18 100%
        );
    border-right: 1px solid rgba(130, 120, 255, 0.18);
}

section[data-testid="stSidebar"] > div {
    padding: 25px 20px;
}

/* Brand */

.brand-box {
    padding: 10px 5px 30px 5px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-logo {
    width: 55px;
    height: 55px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #7b2cff,
            #4e39ff
        );

    box-shadow:
        0 0 30px rgba(112, 54, 255, 0.35);
    font-size: 28px;
}

.brand-name {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

.brand-subtitle {
    margin-top: 3px;
    color: #8e96b5;
    font-size: 12px;
}

/* Sidebar headings */

.sidebar-heading {
    color: #7d86a8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 14px 5px 10px 5px;
}

/* Sidebar divider */

.sidebar-line {
    height: 1px;
    background: rgba(130, 140, 180, 0.15);
    margin: 22px 0;
}

/* Buttons */

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 12px;
    border: 1px solid transparent;
    background: transparent;
    color: #cdd2e8;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(112, 54, 255, 0.12);
    border-color: rgba(126, 83, 255, 0.25);
    color: white;
}

section[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none;
}

/* Premium */

.premium-card {
    margin-top: 25px;
    padding: 20px;
    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            rgba(104, 38, 210, 0.30),
            rgba(60, 35, 130, 0.16)
        );

    border: 1px solid rgba(140, 90, 255, 0.28);
}

.premium-title {
    color: #b877ff;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
}

.premium-text {
    color: #aeb5d0;
    font-size: 12px;
    line-height: 1.6;
    margin-bottom: 15px;
}

/* User profile */

.profile-card {
    margin-top: 25px;
    padding: 12px 5px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.profile-avatar {
    width: 43px;
    height: 43px;
    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(135deg, #7136ff, #4523a9);
    font-weight: 800;
    font-size: 17px;
}

.profile-name {
    font-size: 14px;
    font-weight: 700;
}

.profile-plan {
    font-size: 11px;
    color: #8f97b5;
    margin-top: 3px;
}

/* ============================================================
   MAIN HEADER
   ============================================================ */

.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.greeting {
    font-size: 37px;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.greeting-purple {
    color: #8b55ff;
}

.greeting-subtitle {
    color: #8d96b5;
    font-size: 14px;
    margin-top: 7px;
}

.date-card {
    min-width: 165px;
    padding: 14px 18px;
    border-radius: 16px;

    background: rgba(25, 30, 52, 0.65);
    border: 1px solid rgba(120, 130, 180, 0.16);

    text-align: center;
}

.date-main {
    font-size: 13px;
    font-weight: 700;
}

.date-time {
    color: #858da9;
    font-size: 11px;
    margin-top: 4px;
}

/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 25px;
}

.stat-card {
    min-height: 190px;
    padding: 20px;
    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(25, 29, 52, 0.96),
            rgba(12, 16, 35, 0.95)
        );

    border: 1px solid rgba(120, 130, 180, 0.18);
    position: relative;
    overflow: hidden;
}

.stat-card.purple {
    border-color: rgba(157, 73, 255, 0.30);
}

.stat-card.blue {
    border-color: rgba(40, 139, 255, 0.28);
}

.stat-card.green {
    border-color: rgba(32, 210, 133, 0.25);
}

.stat-card.orange {
    border-color: rgba(255, 163, 38, 0.27);
}

.stat-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 22px;
    margin-bottom: 15px;
}

.purple .stat-icon {
    background: rgba(137, 54, 255, 0.18);
}

.blue .stat-icon {
    background: rgba(40, 135, 255, 0.16);
}

.green .stat-icon {
    background: rgba(28, 206, 130, 0.14);
}

.orange .stat-icon {
    background: rgba(255, 161, 32, 0.14);
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
}

.stat-title {
    margin-top: 4px;
    font-size: 14px;
    font-weight: 600;
}

.stat-description {
    margin-top: 5px;
    color: #7f88a7;
    font-size: 11px;
}

/* ============================================================
   CHAT PANEL
   ============================================================ */

.chat-panel {
    min-height: 570px;

    background:
        linear-gradient(
            145deg,
            rgba(12, 16, 36, 0.98),
            rgba(8, 11, 27, 0.98)
        );

    border: 1px solid rgba(120, 130, 180, 0.18);
    border-radius: 22px;

    padding: 0;
    overflow: hidden;

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.18);
}

.chat-header {
    padding: 22px 25px;
    border-bottom: 1px solid rgba(120, 130, 180, 0.13);

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-title {
    font-size: 20px;
    font-weight: 800;
}

.chat-subtitle {
    color: #8089a7;
    font-size: 12px;
    margin-top: 4px;
}

/* ============================================================
   CHAT MESSAGES
   ============================================================ */

.chat-area {
    padding: 25px;
    min-height: 360px;
}

.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 18px 0;
}

.user-bubble {
    max-width: 70%;
    padding: 13px 17px;

    border-radius: 16px 16px 5px 16px;

    background:
        linear-gradient(
            135deg,
            #7038ef,
            #5425ca
        );

    color: white;
    font-size: 14px;

    box-shadow:
        0 8px 25px rgba(100, 40, 230, 0.20);
}

.ai-message {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin: 18px 0;
}

.ai-avatar {
    width: 38px;
    height: 38px;
    min-width: 38px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(135deg, #2479ff, #3b45c9);
    font-size: 18px;
}

.ai-bubble {
    max-width: 75%;

    padding: 13px 17px;

    border-radius: 5px 16px 16px 16px;

    background: #1a2035;
    border: 1px solid rgba(120, 130, 180, 0.15);

    color: #e5e8f3;
    font-size: 14px;
    line-height: 1.55;
}

/* ============================================================
   CHAT INPUT
   ============================================================ */

div[data-testid="stChatInput"] {
    padding: 0 25px 25px 25px;
}

div[data-testid="stChatInput"] > div {
    background: #171d31 !important;
    border: 1px solid rgba(130, 140, 190, 0.20) !important;
    border-radius: 17px !important;
}

div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #ffffff !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #737c9a !important;
}

/* ============================================================
   EMPTY CHAT
   ============================================================ */

.empty-chat {
    min-height: 330px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-align: center;
}

.empty-icon {
    width: 65px;
    height: 65px;
    border-radius: 20px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #7038ef,
            #3325a4
        );

    box-shadow:
        0 0 40px rgba(108, 50, 240, 0.25);

    font-size: 30px;
    margin-bottom: 18px;
}

.empty-title {
    font-size: 25px;
    font-weight: 800;
}

.empty-text {
    color: #7d86a5;
    font-size: 13px;
    margin-top: 7px;
}

/* ============================================================
   FOOTER
   ============================================================ */

.app-footer {
    text-align: center;
    color: #69718e;
    font-size: 11px;
    margin-top: 22px;
    padding-bottom: 5px;
}

.footer-heart {
    color: #a35cff;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1000px) {

    .stat-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .greeting {
        font-size: 30px;
    }

}

@media (max-width: 650px) {

    .stat-grid {
        grid-template-columns: 1fr;
    }

    .main-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }

    .date-card {
        width: 100%;
    }

}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-row">
                <div class="brand-logo">🤖</div>
                <div>
                    <div class="brand-name">Danish AI</div>
                    <div class="brand-subtitle">
                        Your intelligent AI Assistant
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">WORKSPACE</div>',
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

    st.markdown('<div class="sidebar-line"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-heading">CHAT</div>',
        unsafe_allow_html=True
    )

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.session_state.roast_mode = False
        st.rerun()

    st.markdown(
        """
        <div class="premium-card">
            <div class="premium-title">♛ Danish AI Premium</div>
            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>
        </div>

        <div class="profile-card">
            <div class="profile-avatar">D</div>
            <div>
                <div class="profile-name">Danish</div>
                <div class="profile-plan">Free Plan</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# MAIN HEADER
# ============================================================

now = datetime.now()

date_text = now.strftime("%B %d, %Y")
time_text = now.strftime("%I:%M %p")

st.markdown(
    f"""
    <div class="main-header">
        <div>
            <div class="greeting">
                Good evening,
                <span class="greeting-purple">Danish</span> 👋
            </div>

            <div class="greeting-subtitle">
                Here's what's happening with Danish AI today.
            </div>
        </div>

        <div class="date-card">
            <div class="date-main">📅 &nbsp; {date_text}</div>
            <div class="date-time">{time_text}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        f"""
        <div class="stat-grid">

            <div class="stat-card purple">
                <div class="stat-icon">💬</div>
                <div class="stat-number">{total_messages}</div>
                <div class="stat-title">Messages</div>
                <div class="stat-description">Total messages</div>
            </div>

            <div class="stat-card blue">
                <div class="stat-icon">❓</div>
                <div class="stat-number">{questions}</div>
                <div class="stat-title">Questions</div>
                <div class="stat-description">Asked by you</div>
            </div>

            <div class="stat-card green">
                <div class="stat-icon">🤖</div>
                <div class="stat-number">{ai_responses}</div>
                <div class="stat-title">AI Responses</div>
                <div class="stat-description">From Danish AI</div>
            </div>

            <div class="stat-card orange">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{roast_count}</div>
                <div class="stat-title">Roast Mode</div>
                <div class="stat-description">Funny roasts</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
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
                    <div class="chat-title">💬 AI Chat</div>
                    <div class="chat-subtitle">
                        Talk with Danish AI.
                    </div>
                </div>
            </div>

            <div class="chat-area">
        """,
        unsafe_allow_html=True
    )

    visible_messages = [
        m for m in st.session_state.messages
        if m["role"] != "system"
    ]

    if len(visible_messages) == 0:

        st.markdown(
            """
            <div class="empty-chat">
                <div class="empty-icon">🤖</div>

                <div class="empty-title">
                    How can I help you?
                </div>

                <div class="empty-text">
                    Ask Danish AI anything.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for message in visible_messages:

            if message["role"] == "user":

                st.markdown(
                    f"""
                    <div class="user-message">
                        <div class="user-bubble">
                            {message["content"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif message["role"] == "assistant":

                safe_answer = message["content"].replace("\n", "<br>")

                st.markdown(
                    f"""
                    <div class="ai-message">

                        <div class="ai-avatar">
                            🤖
                        </div>

                        <div class="ai-bubble">
                            {safe_answer}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # ROAST MODE BUTTON
    # ========================================================

    roast_col, _ = st.columns([1, 5])

    with roast_col:

        if st.button(
            "🔥 Roast Mode",
            use_container_width=True
        ):
            st.session_state.roast_mode = not st.session_state.roast_mode

            if st.session_state.roast_mode:
                st.toast("🔥 Roast Mode ON")
            else:
                st.toast("Roast Mode OFF")

    # ========================================================
    # CHAT INPUT
    # ========================================================

    placeholder = (
        "🔥 Roast mode — say something..."
        if st.session_state.roast_mode
        else
        "Type your message..."
    )

    user_input = st.chat_input(placeholder)

    if user_input:

        final_input = user_input

        if st.session_state.roast_mode:
            final_input = (
                "Roast mode is ON. Give me a funny, playful and harmless "
                "roast based on this message:\n\n"
                + user_input
            )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.spinner("Danish AI is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ]
                    + [
                        {
                            "role": m["role"],
                            "content": (
                                final_input
                                if (
                                    m["role"] == "user"
                                    and m is st.session_state.messages[-1]
                                )
                                else m["content"]
                            )
                        }
                        for m in st.session_state.messages
                        if m["role"] != "system"
                    ]
                )

                answer = response.choices[0].message.content

            except Exception as e:

                answer = (
                    "Sorry, I couldn't connect to the AI right now. "
                    "Please check your OpenAI API key and try again."
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        st.rerun()

# ============================================================
# USAGE & STATS
# ============================================================

elif st.session_state.page == "Usage & Stats":

    st.markdown(
        """
        <div class="chat-panel">
            <div class="chat-header">
                <div>
                    <div class="chat-title">📊 Usage & Stats</div>
                    <div class="chat-subtitle">
                        Your Danish AI activity.
                    </div>
                </div>
            </div>

            <div class="chat-area">

                <div class="stat-grid">

                    <div class="stat-card purple">
                        <div class="stat-icon">💬</div>
                        <div class="stat-number">
                            """ + str(total_messages) + """
                        </div>
                        <div class="stat-title">
                            Total Messages
                        </div>
                    </div>

                    <div class="stat-card blue">
                        <div class="stat-icon">❓</div>
                        <div class="stat-number">
                            """ + str(questions) + """
                        </div>
                        <div class="stat-title">
                            Questions
                        </div>
                    </div>

                    <div class="stat-card green">
                        <div class="stat-icon">🤖</div>
                        <div class="stat-number">
                            """ + str(ai_responses) + """
                        </div>
                        <div class="stat-title">
                            AI Responses
                        </div>
                    </div>

                    <div class="stat-card orange">
                        <div class="stat-icon">🔥</div>
                        <div class="stat-number">
                            """ + str(roast_count) + """
                        </div>
                        <div class="stat-title">
                            Roast Sessions
                        </div>
                    </div>

                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="chat-panel">

            <div class="chat-header">
                <div>
                    <div class="chat-title">⚙️ Settings</div>
                    <div class="chat-subtitle">
                        Manage your Danish AI experience.
                    </div>
                </div>
            </div>

            <div class="chat-area">

                <h3>Danish AI</h3>

                <p style="color:#858da9;">
                    Your intelligent AI assistant.
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        Danish AI · Your Intelligent AI Assistant
        <span class="footer-heart">♡</span>
    </div>
    """,
    unsafe_allow_html=True
)
