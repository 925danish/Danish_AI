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
    initial_sidebar_state="expanded"
)


# =========================================================
# OPENAI
# =========================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =========================================================
# AI SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

Answer clearly and helpfully.

You can speak English or Urdu depending on the user's language.

If the user asks "roast me" or asks for a roast,
give a funny, playful and harmless roast.

Never use hateful, threatening or seriously abusive language.
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
# STATISTICS
# =========================================================

user_messages = sum(
    1 for message in st.session_state.messages
    if message["role"] == "user"
)

ai_messages = sum(
    1 for message in st.session_state.messages
    if message["role"] == "assistant"
)

total_messages = user_messages + ai_messages


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
<style>

/* ========================================================
   MAIN APP
   ======================================================== */

.stApp {
    background: #070b1c;
    color: #ffffff;
}

.main {
    background: #070b1c;
}

.block-container {
    max-width: 1500px;
    padding-top: 35px;
    padding-left: 35px;
    padding-right: 35px;
    padding-bottom: 30px;
}


/* Remove Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}


/* ========================================================
   SIDEBAR
   ======================================================== */

[data-testid="stSidebar"] {
    background: #080d20;
    border-right: 1px solid #202943;
    min-width: 275px;
    max-width: 275px;
}

[data-testid="stSidebar"] > div {
    padding: 25px 20px;
}


/* Brand */

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 32px;
}

.brand-logo {
    width: 55px;
    height: 55px;
    border-radius: 17px;
    background: linear-gradient(135deg, #9b45ff, #5d21d6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    box-shadow: 0 0 25px rgba(132, 48, 255, 0.35);
}

.brand-title {
    font-size: 22px;
    font-weight: 800;
    color: #f5f3ff;
}

.brand-subtitle {
    color: #818ba1;
    font-size: 10px;
    margin-top: 4px;
}


/* Sidebar heading */

.sidebar-heading {
    color: #68738b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin-bottom: 9px;
}


/* Sidebar buttons */

[data-testid="stSidebar"] .stButton {
    margin-bottom: 5px;
}

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    height: 43px;
    border-radius: 10px;
    background: transparent;
    color: #cbd1df;
    border: 1px solid transparent;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    transition: 0.2s;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: #21123c;
    border-color: #51248b;
    color: white;
}


/* Sidebar divider */

.divider {
    height: 1px;
    background: #202943;
    margin: 22px 0 18px 0;
}


/* Premium */

.premium {
    margin-top: 35px;
    padding: 17px;
    border-radius: 15px;
    background: linear-gradient(145deg, #2a1449, #141126);
    border: 1px solid #54288c;
}

.premium-title {
    color: #b65aff;
    font-size: 14px;
    font-weight: 800;
}

.premium-text {
    color: #929bb0;
    font-size: 11px;
    line-height: 1.5;
    margin-top: 7px;
    margin-bottom: 13px;
}


/* Sidebar upgrade button */

[data-testid="stSidebar"] button[kind="secondary"] {
    color: #ffffff;
}


/* Profile */

.profile {
    border-top: 1px solid #202943;
    margin-top: 27px;
    padding-top: 18px;
    display: flex;
    align-items: center;
}

.avatar {
    width: 41px;
    height: 41px;
    border-radius: 50%;
    background: #351761;
    color: #bd7cff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-right: 11px;
}

.profile-name {
    color: #f0f2f7;
    font-size: 13px;
    font-weight: 700;
}

.profile-plan {
    color: #788298;
    font-size: 10px;
    margin-top: 3px;
}


/* ========================================================
   HEADER
   ======================================================== */

.header-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 28px;
}

.greeting {
    color: #f5f5f8;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}

.greeting-purple {
    color: #8746ff;
}

.subtitle {
    color: #7f899f;
    font-size: 12px;
    margin-top: 7px;
}


/* Date */

.date-box {
    width: 160px;
    min-height: 77px;
    border-radius: 16px;
    background: #101629;
    border: 1px solid #29334b;
    padding: 12px 15px;
}

.date-icon {
    font-size: 17px;
}

.date-value {
    color: #e7eaf1;
    font-size: 11px;
    font-weight: 700;
    margin-top: 3px;
}

.time-value {
    color: #788298;
    font-size: 10px;
    margin-top: 3px;
}


/* ========================================================
   STAT CARDS
   ======================================================== */

.stat-card {
    height: 183px;
    padding: 20px;
    border-radius: 18px;
    box-sizing: border-box;
}

.stat-purple {
    background: linear-gradient(145deg, #171029, #0c1223);
    border: 1px solid #542b85;
}

.stat-blue {
    background: linear-gradient(145deg, #0d1b32, #0c1325);
    border: 1px solid #1d4d83;
}

.stat-green {
    background: linear-gradient(145deg, #092421, #0c1525);
    border: 1px solid #155c4d;
}

.stat-orange {
    background: linear-gradient(145deg, #21180d, #0d1424);
    border: 1px solid #67491e;
}


.stat-icon {
    width: 43px;
    height: 43px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 17px;
}

.icon-purple {
    background: #341454;
    border: 1px solid #7136a5;
}

.icon-blue {
    background: #102f56;
    border: 1px solid #205b9a;
}

.icon-green {
    background: #0a3b32;
    border: 1px solid #17725d;
}

.icon-orange {
    background: #493013;
    border: 1px solid #7a531d;
}


.stat-number {
    color: #f0f3f8;
    font-size: 28px;
    font-weight: 800;
}

.stat-title {
    color: #d8dce5;
    font-size: 14px;
    font-weight: 700;
    margin-top: 5px;
}

.stat-description {
    color: #7d879c;
    font-size: 10px;
    margin-top: 4px;
}


/* ========================================================
   CHAT AREA
   ======================================================== */

.chat-container {
    margin-top: 30px;
    border-radius: 19px;
    background: #080e20;
    border: 1px solid #242e48;
    overflow: hidden;
}

.chat-header {
    min-height: 90px;
    padding: 20px 25px;
    border-bottom: 1px solid #222b42;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
}

.chat-title-area {
    display: flex;
    align-items: center;
    gap: 13px;
}

.chat-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: #351460;
    border: 1px solid #7034aa;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-title {
    color: #f2f3f7;
    font-size: 20px;
    font-weight: 800;
}

.chat-subtitle {
    color: #7d879d;
    font-size: 11px;
    margin-top: 3px;
}

.new-chat {
    padding: 12px 19px;
    border-radius: 11px;
    background: linear-gradient(135deg, #8438ff, #5e20d3);
    border: 1px solid #914dff;
    color: white;
    font-size: 12px;
    font-weight: 700;
}


/* Empty state */

.empty-state {
    min-height: 390px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.empty-logo {
    width: 64px;
    height: 64px;
    border-radius: 20px;
    background: #151d31;
    border: 1px solid #303b55;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    margin-bottom: 16px;
}

.empty-title {
    color: #eef0f5;
    font-size: 25px;
    font-weight: 800;
}

.empty-text {
    color: #778298;
    font-size: 11px;
    margin-top: 6px;
}


/* ========================================================
   CHAT INPUT
   ======================================================== */

[data-testid="stChatInput"] {
    margin-left: 25px;
    margin-right: 25px;
    margin-bottom: 25px;
}

[data-testid="stChatInput"] > div {
    background: #1a2336 !important;
    border: 1px solid #3a465f !important;
    border-radius: 17px !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
    font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7d879c !important;
}


/* ========================================================
   FOOTER
   ======================================================== */

.app-footer {
    text-align: center;
    color: #707b91;
    font-size: 10px;
    margin-top: 22px;
}

.heart {
    color: #a855f7;
    font-size: 14px;
}


/* ========================================================
   MOBILE
   ======================================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .greeting {
        font-size: 26px;
    }

    .date-box {
        width: 130px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-logo">
                🤖
            </div>

            <div>
                <div class="brand-title">
                    Danish AI
                </div>

                <div class="brand-subtitle">
                    Your intelligent AI Assistant
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

    if st.button("⌂   Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("▣   AI Chat", use_container_width=True):
        st.session_state.page = "Chat"
        st.rerun()

    if st.button("▥   Usage & Stats", use_container_width=True):
        st.session_state.page = "Stats"
        st.rerun()

    if st.button("⚙   Settings", use_container_width=True):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">CHAT</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🗑   Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()

    st.markdown(
        """
        <div class="premium">

            <div class="premium-title">
                ♛ Danish AI Premium
            </div>

            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Upgrade Now",
        use_container_width=True
    ):
        st.info("Premium features coming soon.")

    st.markdown(
        """
        <div class="profile">

            <div class="avatar">
                D
            </div>

            <div>
                <div class="profile-name">
                    Danish
                </div>

                <div class="profile-plan">
                    Free Plan
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    # Header

    col_left, col_right = st.columns([5, 1])

    with col_left:

        st.markdown(
            """
            <div class="greeting">
                Good evening,
                <span class="greeting-purple">
                    Danish
                </span>
                👋
            </div>

            <div class="subtitle">
                Here's what's happening with Danish AI today.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:

        now = datetime.now()

        st.markdown(
            f"""
            <div class="date-box">

                <div class="date-icon">
                    📅
                </div>

                <div class="date-value">
                    {now.strftime("%B %d, %Y")}
                </div>

                <div class="time-value">
                    {now.strftime("%I:%M %p")}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # STATISTICS
    # =====================================================

    s1, s2, s3, s4 = st.columns(4)

    with s1:

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

    with s2:

        st.markdown(
            f"""
            <div class="stat-card stat-blue">

                <div class="stat-icon icon-blue">
                    ♙
                </div>

                <div class="stat-number">
                    {user_messages}
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

    with s3:

        st.markdown(
            f"""
            <div class="stat-card stat-green">

                <div class="stat-icon icon-green">
                    🤖
                </div>

                <div class="stat-number">
                    {ai_messages}
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

    with s4:

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
    # CHAT HEADER
    # =====================================================

    st.markdown(
        """
        <div class="chat-container">

            <div class="chat-header">

                <div class="chat-title-area">

                    <div class="chat-icon">
                        💬
                    </div>

                    <div>

                        <div class="chat-title">
                            AI Chat
                        </div>

                        <div class="chat-subtitle">
                            Talk with Danish AI.
                        </div>

                    </div>

                </div>

                <div class="new-chat">
                    ⊕ New Chat
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # CHAT MESSAGES
    # =====================================================

    visible_messages = [
        message
        for message in st.session_state.messages
        if message["role"] != "system"
    ]

    if not visible_messages:

        st.markdown(
            """
            <div class="empty-state">

                <div class="empty-logo">
                    🤖
                </div>

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

            with st.chat_message(
                message["role"],
                avatar="🤖" if message["role"] == "assistant" else "D"
            ):
                st.markdown(message["content"])


    # =====================================================
    # ROAST MODE
    # =====================================================

    roast_col, spacer = st.columns([1, 6])

    with roast_col:

        if st.button(
            "🔥 Roast Mode",
            use_container_width=True
        ):
            st.session_state.roast_mode = (
                not st.session_state.roast_mode
            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    placeholder = (
        "Roast me..."
        if st.session_state.roast_mode
        else "Type your message..."
    )

    user_input = st.chat_input(placeholder)


    if user_input:

        final_input = user_input

        if st.session_state.roast_mode:

            final_input = (
                "Roast me playfully and harmlessly. "
                "Here is what I said: "
                + user_input
            )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": final_input
            }
        )

        try:

            with st.spinner("Danish AI is thinking..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )

            answer = response.choices[0].message.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

        except Exception as error:

            st.error(
                "Danish AI couldn't connect to OpenAI. "
                "Please check your API key."
            )


# =========================================================
# AI CHAT PAGE
# =========================================================

elif st.session_state.page == "Chat":

    st.markdown(
        """
        <div class="greeting">
            AI Chat
            <span class="greeting-purple">
                💬
            </span>
        </div>

        <div class="subtitle">
            Talk with Danish AI.
        </div>
        """,
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(
            message["role"],
            avatar="🤖" if message["role"] == "assistant" else "D"
        ):
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

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            answer = response.choices[0].message.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

        except Exception:

            st.error(
                "Unable to connect to Danish AI."
            )


# =========================================================
# USAGE & STATS
# =========================================================

elif st.session_state.page == "Stats":

    st.markdown(
        """
        <div class="greeting">
            Usage & Stats
            <span class="greeting-purple">
                📊
            </span>
        </div>

        <div class="subtitle">
            Your Danish AI activity.
        </div>
        """,
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Messages",
            total_messages
        )

    with b:
        st.metric(
            "Questions",
            user_messages
        )

    with c:
        st.metric(
            "AI Responses",
            ai_messages
        )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="greeting">
            Settings
            <span class="greeting-purple">
                ⚙️
            </span>
        </div>

        <div class="subtitle">
            Customize your Danish AI experience.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.selectbox(
        "Language",
        [
            "Automatic",
            "English",
            "Urdu"
        ]
    )

    st.selectbox(
        "Theme",
        [
            "Danish AI Dark"
        ]
    )

    st.toggle(
        "Enable Roast Mode"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="app-footer">
        Danish AI • Your Intelligent AI Assistant
        <span class="heart">♡</span>
    </div>
    """,
    unsafe_allow_html=True
)
