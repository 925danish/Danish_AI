import streamlit as st
from openai import OpenAI
from datetime import datetime

# =========================================================
# PAGE
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

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

SYSTEM_PROMPT = """
You are Danish AI, a helpful, intelligent and professional AI assistant.
Give clear, useful and friendly answers.
Help with programming, artificial intelligence, learning, business and
general questions.
Keep answers easy to understand unless the user asks for detail.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False

# =========================================================
# STATISTICS
# =========================================================

user_messages = sum(
    1 for m in st.session_state.messages if m["role"] == "user"
)

ai_messages = sum(
    1 for m in st.session_state.messages if m["role"] == "assistant"
)

total_messages = len(st.session_state.messages)

roast_messages = sum(
    1 for m in st.session_state.messages if m.get("roast", False)
)

# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
<style>

/* ==============================
   REMOVE STREAMLIT UI
   ============================== */

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

[data-testid="stDecoration"] {
    display: none;
}

/* ==============================
   MAIN BACKGROUND
   ============================== */

.stApp {
    background:
        radial-gradient(
            circle at 75% 0%,
            rgba(124, 58, 237, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 20% 90%,
            rgba(37, 99, 235, 0.10),
            transparent 30%
        ),
        #070b1b;
    color: white;
}

/* ==============================
   PAGE WIDTH
   ============================== */

.block-container {
    max-width: 1450px !important;
    padding-top: 32px !important;
    padding-bottom: 25px !important;
}

/* ==============================
   SIDEBAR
   ============================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080c1d 0%,
            #080c1e 100%
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding: 24px 18px;
}

/* BRAND */

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 5px 5px 30px 5px;
}

.logo {
    width: 56px;
    height: 56px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(
            135deg,
            #8b5cf6,
            #5b21b6
        );
    box-shadow:
        0 10px 35px rgba(124,58,237,0.35);
    font-size: 29px;
}

.brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
}

.brand-sub {
    font-size: 11px;
    color: #7f89a8;
    margin-top: 3px;
}

/* SIDEBAR LABEL */

.sidebar-label {
    font-size: 10px;
    font-weight: 800;
    color: #68718f;
    letter-spacing: 1.7px;
    margin: 12px 8px 10px 8px;
}

/* SIDEBAR BUTTONS */

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 11px;
    border: 1px solid transparent;
    background: transparent;
    color: #aeb6ce;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(124,58,237,0.16);
    color: white;
    border-color: rgba(124,58,237,0.25);
}

/* SIDEBAR DIVIDER */

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 22px 4px;
}

/* PREMIUM */

.premium {
    margin-top: 28px;
    padding: 18px;
    border-radius: 17px;
    background:
        linear-gradient(
            145deg,
            rgba(124,58,237,0.28),
            rgba(48,28,100,0.20)
        );
    border: 1px solid rgba(139,92,246,0.30);
}

.premium-title {
    color: #dccbff;
    font-size: 14px;
    font-weight: 800;
}

.premium-text {
    color: #929ab5;
    font-size: 11px;
    line-height: 1.6;
    margin: 8px 0 14px 0;
}

.premium-btn {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #5b21b6
    );
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-size: 12px;
    font-weight: 700;
}

/* PROFILE */

.profile {
    margin-top: 24px;
    padding-top: 18px;
    border-top: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    gap: 11px;
}

.profile-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(
        135deg,
        #7c3aed,
        #4c1d95
    );
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
    color: #747e9d;
    font-size: 11px;
    margin-top: 3px;
}

/* ==============================
   HEADER
   ============================== */

.greeting {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: white;
}

.greeting span {
    color: #7c3aed;
}

.subtitle {
    color: #7f89a8;
    font-size: 13px;
    margin-top: 5px;
}

.date-card {
    padding: 14px 17px;
    border-radius: 15px;
    background: rgba(19,24,45,0.8);
    border: 1px solid rgba(255,255,255,0.08);
}

.date-title {
    font-size: 12px;
    font-weight: 700;
}

.date-time {
    color: #7d86a3;
    font-size: 11px;
    margin-top: 4px;
}

/* ==============================
   STAT CARDS
   ============================== */

.stat {
    min-height: 160px;
    padding: 19px;
    border-radius: 18px;
    background: rgba(14,19,39,0.90);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 14px 40px rgba(0,0,0,0.20);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 13px;
}

.icon-purple {
    background: rgba(139,92,246,0.16);
    border: 1px solid rgba(139,92,246,0.32);
}

.icon-blue {
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.30);
}

.icon-green {
    background: rgba(16,185,129,0.13);
    border: 1px solid rgba(16,185,129,0.28);
}

.icon-orange {
    background: rgba(245,158,11,0.13);
    border: 1px solid rgba(245,158,11,0.28);
}

.stat-number {
    font-size: 28px;
    font-weight: 800;
}

.stat-title {
    color: #c4c9dc;
    font-size: 13px;
    font-weight: 700;
    margin-top: 2px;
}

.stat-sub {
    color: #68718e;
    font-size: 11px;
    margin-top: 4px;
}

/* ==============================
   CHAT PANEL
   ============================== */

.chat-panel {
    margin-top: 12px;
    border-radius: 20px;
    background: rgba(7,11,28,0.78);
    border: 1px solid rgba(255,255,255,0.09);
    overflow: hidden;
}

.chat-header {
    padding: 20px 23px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.chat-title {
    color: white;
    font-size: 19px;
    font-weight: 800;
}

.chat-sub {
    color: #78819f;
    font-size: 12px;
    margin-top: 4px;
}

.chat-logo {
    display: inline-flex;
    width: 39px;
    height: 39px;
    border-radius: 11px;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
        135deg,
        #7c3aed,
        #4c1d95
    );
    margin-right: 10px;
}

/* EMPTY CHAT */

.empty {
    padding: 75px 20px;
    text-align: center;
}

.empty-icon {
    width: 70px;
    height: 70px;
    margin: auto;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #7c3aed,
        #4c1d95
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 31px;
    box-shadow:
        0 15px 45px rgba(124,58,237,0.28);
}

.empty-title {
    margin-top: 18px;
    font-size: 25px;
    font-weight: 800;
}

.empty-sub {
    margin-top: 6px;
    color: #78819e;
    font-size: 13px;
}

/* ==============================
   MESSAGES
   ============================== */

.user-message {
    width: fit-content;
    max-width: 75%;
    margin: 18px 24px 18px auto;
    padding: 13px 17px;
    border-radius: 17px 17px 5px 17px;
    background: linear-gradient(
        135deg,
        #7c3aed,
        #5b21b6
    );
    color: white;
    font-size: 14px;
    box-shadow: 0 10px 30px rgba(92,33,182,0.20);
}

.ai-message {
    width: fit-content;
    max-width: 75%;
    margin: 18px auto 18px 24px;
    padding: 13px 17px;
    border-radius: 17px 17px 17px 5px;
    background: #171d33;
    border: 1px solid rgba(255,255,255,0.08);
    color: #e2e5ef;
    font-size: 14px;
}

/* ==============================
   CHAT INPUT
   ============================== */

.stChatInput {
    padding-bottom: 10px;
}

.stChatInput > div {
    background: #151b30 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
}

.stChatInput textarea {
    color: white !important;
}

.stChatInput textarea::placeholder {
    color: #69728f !important;
}

/* ==============================
   NORMAL BUTTONS
   ============================== */

.stButton > button {
    border-radius: 11px;
    border: 1px solid rgba(255,255,255,0.10);
    background: #11172c;
    color: #cbd0e2;
}

.stButton > button:hover {
    border-color: #7c3aed;
    color: white;
}

/* ==============================
   SETTINGS
   ============================== */

.settings {
    margin-top: 20px;
    padding: 24px;
    border-radius: 18px;
    background: #11172c;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ==============================
   FOOTER
   ============================== */

.footer {
    text-align: center;
    color: #626b89;
    font-size: 11px;
    margin-top: 30px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="logo">🤖</div>
            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-sub">Your intelligent AI Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    if st.button("🏠   Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("💬   AI Chat", use_container_width=True):
        st.session_state.page = "AI Chat"
        st.rerun()

    if st.button("📊   Usage & Stats", use_container_width=True):
        st.session_state.page = "Usage & Stats"
        st.rerun()

    if st.button("⚙️   Settings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">CHAT</div>',
        unsafe_allow_html=True,
    )

    if st.button("🗑️   Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="premium">
            <div class="premium-title">👑 Danish AI Premium</div>

            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>

            <div class="premium-btn">
                Upgrade Now
            </div>
        </div>

        <div class="profile">
            <div class="profile-icon">D</div>

            <div>
                <div class="profile-name">Danish</div>
                <div class="profile-plan">Free Plan</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# HEADER
# =========================================================

now = datetime.now()

if now.hour < 12:
    greeting = "Good morning"
elif now.hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

left, right = st.columns([5, 1])

with left:

    st.markdown(
        f"""
        <div class="greeting">
            {greeting}, <span>Danish</span> 👋
        </div>

        <div class="subtitle">
            Here's what's happening with Danish AI today.
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:

    st.markdown(
        f"""
        <div class="date-card">
            <div class="date-title">
                📅 {now.strftime("%B %d, %Y")}
            </div>

            <div class="date-time">
                {now.strftime("%I:%M %p")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =========================================================
# DASHBOARD STATS
# =========================================================

if st.session_state.page == "Dashboard":

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-icon icon-purple">💬</div>
                <div class="stat-number">{total_messages}</div>
                <div class="stat-title">Messages</div>
                <div class="stat-sub">Total messages</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-icon icon-blue">❓</div>
                <div class="stat-number">{user_messages}</div>
                <div class="stat-title">Questions</div>
                <div class="stat-sub">Asked by you</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-icon icon-green">🤖</div>
                <div class="stat-number">{ai_messages}</div>
                <div class="stat-title">AI Responses</div>
                <div class="stat-sub">From Danish AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-icon icon-orange">🔥</div>
                <div class="stat-number">{roast_messages}</div>
                <div class="stat-title">Roast Mode</div>
                <div class="stat-sub">Funny roasts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# CHAT
# =========================================================

if st.session_state.page in ["Dashboard", "AI Chat"]:

    st.markdown(
        """
        <div class="chat-panel">

            <div class="chat-header">

                <div class="chat-title">
                    <span class="chat-logo">💬</span>
                    AI Chat
                </div>

                <div class="chat-sub">
                    Talk with Danish AI.
                </div>

            </div>
        """,
        unsafe_allow_html=True,
    )

    # Empty state

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="empty">

                <div class="empty-icon">
                    🤖
                </div>

                <div class="empty-title">
                    How can I help you?
                </div>

                <div class="empty-sub">
                    Ask Danish AI anything.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # Messages

    else:

        for message in st.session_state.messages:

            content = message["content"]

            if message["role"] == "user":

                st.markdown(
                    f"""
                    <div class="user-message">
                        {content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    f"""
                    <div class="ai-message">
                        🤖 &nbsp; {content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # =====================================================
    # ROAST MODE
    # =====================================================

    col1, col2 = st.columns([1, 6])

    with col1:

        if st.button(
            "🔥 Roast Mode",
            use_container_width=True,
        ):
            st.session_state.roast_mode = (
                not st.session_state.roast_mode
            )
            st.rerun()

    if st.session_state.roast_mode:

        st.caption(
            "🔥 Roast Mode is ON — playful answers enabled."
        )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Type your message..."
    )

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
                "⚠️ OpenAI is not connected. "
                "Please check your OPENAI_API_KEY in "
                "Streamlit Secrets."
            )

        else:

            try:

                system = SYSTEM_PROMPT

                if st.session_state.roast_mode:

                    system += """
                    Roast Mode is enabled.
                    Be playful and funny, but never hateful,
                    threatening or abusive.
                    """

                api_messages = [
                    {
                        "role": "system",
                        "content": system,
                    }
                ]

                for message in st.session_state.messages:

                    api_messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                    )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                )

                answer = response.choices[0].message.content

            except Exception as error:

                answer = (
                    "⚠️ I couldn't connect to the AI.\n\n"
                    f"{error}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "roast": st.session_state.roast_mode,
            }
        )

        st.rerun()

# =========================================================
# USAGE PAGE
# =========================================================

if st.session_state.page == "Usage & Stats":

    st.markdown(
        """
        <div class="greeting">
            Usage <span>&</span> Stats
        </div>

        <div class="subtitle">
            Track your Danish AI activity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Total Messages",
            total_messages,
        )

    with b:
        st.metric(
            "Questions",
            user_messages,
        )

    with c:
        st.metric(
            "AI Responses",
            ai_messages,
        )

    st.markdown(
        """
        <div class="settings">
            <h3>📈 Activity Overview</h3>

            <p style="color:#7f89a8;">
                Your statistics update automatically whenever
                you use Danish AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# SETTINGS PAGE
# =========================================================

if st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="greeting">
            Danish AI <span>Settings</span>
        </div>

        <div class="subtitle">
            Customize your AI assistant.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="settings">

            <h3>🤖 Danish AI</h3>

            <p style="color:#7f89a8;">
                Your intelligent personal AI assistant.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    roast_setting = st.toggle(
        "🔥 Roast Mode",
        value=st.session_state.roast_mode,
    )

    st.session_state.roast_mode = roast_setting

    st.write("")

    if st.button(
        "🗑️ Delete Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.success(
            "Conversation deleted."
        )

        st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Danish AI · Your Intelligent AI Assistant · Made with ❤️
    </div>
    """,
    unsafe_allow_html=True,
)
