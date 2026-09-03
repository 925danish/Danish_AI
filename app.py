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
You are Danish AI, a friendly, intelligent AI assistant.

Answer questions clearly and helpfully.

You can communicate in English or Urdu depending on the user's language.

If the user asks for a roast or says "roast me":
give a funny, playful and harmless roast.

Never use hateful, threatening or seriously abusive language.
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


# ============================================================
# COUNTERS
# ============================================================

user_messages = len(
    [
        m for m in st.session_state.messages
        if m["role"] == "user"
    ]
)

assistant_messages = len(
    [
        m for m in st.session_state.messages
        if m["role"] == "assistant"
    ]
)

total_messages = user_messages + assistant_messages


# ============================================================
# CUSTOM CSS
# ============================================================

css = """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background: #070c1d;
    color: #ffffff;
}

.main {
    background: #070c1d;
}

.block-container {
    max-width: 1400px;
    padding-top: 35px;
    padding-left: 34px;
    padding-right: 34px;
    padding-bottom: 25px;
}


/* Hide Streamlit branding */

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


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #080d20;
    border-right: 1px solid #202942;
    min-width: 275px;
    max-width: 275px;
}

[data-testid="stSidebar"] > div {
    padding: 24px 20px;
}


/* Brand */

.brand-container {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 4px 4px 28px 4px;
}

.brand-logo {
    width: 53px;
    height: 53px;
    min-width: 53px;
    border-radius: 17px;
    background: linear-gradient(
        135deg,
        #8b3dff,
        #6425d7
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    box-shadow:
        0 0 22px rgba(124, 58, 237, 0.30);
}

.brand-name {
    color: #f4f3ff;
    font-size: 23px;
    font-weight: 800;
    line-height: 1.1;
}

.brand-subtitle {
    color: #8d96aa;
    font-size: 10px;
    margin-top: 5px;
}


/* Sidebar labels */

.sidebar-label {
    color: #6e7890;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-top: 13px;
    margin-bottom: 10px;
}


/* Sidebar buttons */

[data-testid="stSidebar"] .stButton {
    margin-bottom: 5px;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    height: 44px;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    color: #cbd2e1;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    padding-left: 15px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #19112e;
    border-color: #432575;
    color: #ffffff;
}


/* Sidebar separator */

.sidebar-line {
    height: 1px;
    background: #202942;
    margin: 23px 0 18px 0;
}


/* Clear button */

.clear-button {
    border: 1px solid #303951;
    border-radius: 11px;
    height: 45px;
    display: flex;
    align-items: center;
    padding-left: 14px;
    color: #d9deea;
    font-size: 12px;
    font-weight: 600;
}


/* Premium card */

.premium-card {
    margin-top: 33px;
    padding: 17px;
    border-radius: 15px;
    border: 1px solid #512a88;
    background:
        linear-gradient(
            145deg,
            #291449 0%,
            #17122d 100%
        );
    box-shadow:
        0 8px 25px rgba(0,0,0,0.20);
}

.premium-title {
    color: #b35cff;
    font-size: 14px;
    font-weight: 800;
}

.premium-description {
    color: #9da5b8;
    font-size: 11px;
    line-height: 1.55;
    margin-top: 7px;
    margin-bottom: 13px;
}


/* Premium button */

[data-testid="stSidebar"] .premium-button .stButton > button {
    background: linear-gradient(
        135deg,
        #8537ff,
        #6120d9
    );
    border: none;
    color: white;
    text-align: center;
    height: 41px;
}


/* Profile */

.profile-section {
    border-top: 1px solid #202942;
    margin-top: 28px;
    padding-top: 18px;
    display: flex;
    align-items: center;
}

.profile-avatar {
    width: 40px;
    height: 40px;
    min-width: 40px;
    border-radius: 50%;
    background: #32175f;
    color: #c993ff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    font-weight: 800;
    margin-right: 11px;
}

.profile-name {
    color: #f2f4f8;
    font-size: 13px;
    font-weight: 700;
}

.profile-plan {
    color: #778197;
    font-size: 10px;
    margin-top: 3px;
}


/* =========================================================
   HEADER
   ========================================================= */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 28px;
}

.greeting {
    color: #f5f6fa;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.1;
}

.greeting-name {
    color: #874cff;
}

.greeting-sub {
    color: #7e889e;
    font-size: 12px;
    margin-top: 8px;
}


/* Date card */

.date-card {
    width: 155px;
    min-height: 76px;
    background: #10172a;
    border: 1px solid #29334c;
    border-radius: 16px;
    padding: 13px 15px;
    box-sizing: border-box;
}

.date-icon {
    color: #d9deea;
    font-size: 17px;
}

.date-text {
    color: #e5e8ef;
    font-size: 11px;
    font-weight: 700;
    margin-top: 3px;
}

.time-text {
    color: #78839a;
    font-size: 10px;
    margin-top: 3px;
}


/* =========================================================
   STATISTICS
   ========================================================= */

.stat-card {
    min-height: 182px;
    padding: 20px;
    border-radius: 18px;
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
}

.stat-purple {
    background:
        linear-gradient(
            145deg,
            #17112a,
            #0d1325
        );
    border: 1px solid #542b83;
}

.stat-blue {
    background:
        linear-gradient(
            145deg,
            #0c1a31,
            #0d1427
        );
    border: 1px solid #19447b;
}

.stat-green {
    background:
        linear-gradient(
            145deg,
            #092323,
            #0d1627
        );
    border: 1px solid #14584e;
}

.stat-orange {
    background:
        linear-gradient(
            145deg,
            #21190f,
            #0d1526
        );
    border: 1px solid #63471e;
}


/* Stat icons */

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    margin-bottom: 17px;
}

.purple-icon {
    background: #321454;
    color: #c15cff;
    border: 1px solid #6932a2;
}

.blue-icon {
    background: #102e54;
    color: #56a4ff;
    border: 1px solid #1c589a;
}

.green-icon {
    background: #0b3c34;
    color: #38df9d;
    border: 1px solid #16715e;
}

.orange-icon {
    background: #4a3113;
    color: #ffad22;
    border: 1px solid #78511e;
}


.stat-number {
    color: #f1f4fa;
    font-size: 28px;
    font-weight: 800;
    line-height: 1;
}

.stat-title {
    color: #d8dce6;
    font-size: 14px;
    font-weight: 700;
    margin-top: 8px;
}

.stat-subtitle {
    color: #7f899e;
    font-size: 10px;
    margin-top: 5px;
}


/* =========================================================
   CHAT PANEL
   ========================================================= */

.chat-panel {
    margin-top: 30px;
    border: 1px solid #242e48;
    border-radius: 19px;
    background: #080e20;
    overflow: hidden;
    min-height: 580px;
}


/* Chat top */

.chat-panel-header {
    height: 91px;
    border-bottom: 1px solid #222b43;
    padding: 20px 25px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-heading-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
}

.chat-header-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: #351460;
    border: 1px solid #7133ae;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
}

.chat-heading {
    color: #f3f4f8;
    font-size: 20px;
    font-weight: 800;
}

.chat-subheading {
    color: #7f899e;
    font-size: 11px;
    margin-top: 3px;
}


/* New chat */

.new-chat {
    background: linear-gradient(
        135deg,
        #8037ff,
        #6120d9
    );
    border: 1px solid #914eff;
    border-radius: 11px;
    color: white;
    padding: 12px 19px;
    font-size: 12px;
    font-weight: 700;
}


/* Chat body */

.chat-body {
    min-height: 385px;
    padding: 26px 25px;
}


/* User message */

.user-row {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 12px;
    margin: 15px 0 27px 0;
}

.user-message {
    max-width: 430px;
    background: linear-gradient(
        135deg,
        #7130e9,
        #5621c2
    );
    border-radius: 14px 14px 5px 14px;
    padding: 13px 17px;
    color: white;
    font-size: 13px;
    line-height: 1.55;
}

.user-time {
    color: #c4b4f4;
    font-size: 9px;
    text-align: right;
    margin-top: 7px;
}

.user-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #3a176e;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #b76aff;
    font-size: 18px;
}


/* AI message */

.ai-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin: 0 0 25px 0;
}

.ai-avatar {
    width: 42px;
    height: 42px;
    min-width: 42px;
    border-radius: 50%;
    background: #102e54;
    border: 1px solid #245da0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #5ca9ff;
    font-size: 18px;
}

.ai-message {
    max-width: 500px;
    background: #171e31;
    border: 1px solid #29344c;
    border-radius: 5px 14px 14px 14px;
    padding: 13px 17px;
    color: #e2e6ee;
    font-size: 13px;
    line-height: 1.6;
}

.ai-time {
    color: #7b879e;
    font-size: 9px;
    margin-top: 7px;
}


/* Empty state */

.empty-chat {
    text-align: center;
    padding: 75px 10px;
}

.empty-icon {
    font-size: 46px;
    margin-bottom: 14px;
}

.empty-title {
    color: #eef0f5;
    font-size: 25px;
    font-weight: 800;
}

.empty-subtitle {
    color: #78839a;
    font-size: 11px;
    margin-top: 7px;
}


/* =========================================================
   STREAMLIT CHAT INPUT
   ========================================================= */

[data-testid="stChatInput"] {
    margin: 0 25px 25px 25px;
}

[data-testid="stChatInput"] > div {
    background: #1a2336 !important;
    border: 1px solid #39455e !important;
    border-radius: 17px !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    background: transparent !important;
    font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7c879c !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.app-footer {
    text-align: center;
    color: #727d94;
    font-size: 10px;
    margin-top: 25px;
    padding-bottom: 5px;
}

.footer-heart {
    color: #a855f7;
    font-size: 14px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .greeting {
        font-size: 27px;
    }

    .date-card {
        width: 135px;
    }

    .stat-card {
        margin-bottom: 12px;
    }
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-container">
            <div class="brand-logo">🤖</div>

            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-subtitle">
                    Your intelligent AI Assistant
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    if st.button("⌂   Dashboard", key="dashboard_button"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("▣   AI Chat", key="chat_button"):
        st.session_state.page = "Chat"
        st.rerun()

    if st.button("▥   Usage & Stats", key="stats_button"):
        st.session_state.page = "Stats"
        st.rerun()

    if st.button("⚙   Settings", key="settings_button"):
        st.session_state.page = "Settings"
        st.rerun()

    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">CHAT</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "▣   Clear Conversation",
        key="clear_conversation"
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
        <div class="premium-card">

            <div class="premium-title">
                ♛ Danish AI Premium
            </div>

            <div class="premium-description">
                Unlock more power and exclusive features.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Upgrade Now",
        key="upgrade"
    ):
        st.info("Premium plans coming soon.")

    st.markdown(
        """
        <div class="profile-section">

            <div class="profile-avatar">
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


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    now = datetime.now()

    date_text = now.strftime("%B %d, %Y")
    time_text = now.strftime("%I:%M %p")


    # HEADER

    left_col, right_col = st.columns(
        [5.5, 1.25]
    )

    with left_col:

        st.markdown(
            """
            <div class="greeting">
                Good evening,
                <span class="greeting-name">
                    Danish
                </span>
                👋
            </div>

            <div class="greeting-sub">
                Here's what's happening with Danish AI today.
            </div>
            """,
            unsafe_allow_html=True
        )

    with right_col:

        st.markdown(
            f"""
            <div class="date-card">

                <div class="date-icon">
                    ▣
                </div>

                <div class="date-text">
                    {date_text}
                </div>

                <div class="time-text">
                    {time_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # STAT CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
            <div class="stat-card stat-purple">

                <div class="stat-icon purple-icon">
                    ▣
                </div>

                <div class="stat-number">
                    {total_messages}
                </div>

                <div class="stat-title">
                    Messages
                </div>

                <div class="stat-subtitle">
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

                <div class="stat-icon blue-icon">
                    ♙
                </div>

                <div class="stat-number">
                    {user_messages}
                </div>

                <div class="stat-title">
                    Questions
                </div>

                <div class="stat-subtitle">
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

                <div class="stat-icon green-icon">
                    🤖
                </div>

                <div class="stat-number">
                    {assistant_messages}
                </div>

                <div class="stat-title">
                    AI Responses
                </div>

                <div class="stat-subtitle">
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

                <div class="stat-icon orange-icon">
                    🔥
                </div>

                <div class="stat-number">
                    0
                </div>

                <div class="stat-title">
                    Roast Mode
                </div>

                <div class="stat-subtitle">
                    Funny roasts
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # CHAT HEADER
    # ========================================================

    st.markdown(
        """
        <div class="chat-panel">

            <div class="chat-panel-header">

                <div class="chat-heading-wrap">

                    <div class="chat-header-icon">
                        ▣
                    </div>

                    <div>

                        <div class="chat-heading">
                            AI Chat
                        </div>

                        <div class="chat-subheading">
                            Talk with Danish AI.
                        </div>

                    </div>

                </div>

                <div class="new-chat">
                    ⊕ New Chat
                </div>

            </div>

            <div class="chat-body">
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CHAT MESSAGES
    # ========================================================

    visible_messages = [
        m for m in st.session_state.messages
        if m["role"] != "system"
    ]


    if not visible_messages:

        st.markdown(
            """
            <div class="empty-chat">

                <div class="empty-icon">
                    🤖
                </div>

                <div class="empty-title">
                    How can I help you today?
                </div>

                <div class="empty-subtitle">
                    Ask Danish AI anything.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for message in visible_messages:

            if message["role"] == "user":

                safe_text = message["content"].replace(
                    "<",
                    "&lt;"
                ).replace(
                    ">",
                    "&gt;"
                )

                st.markdown(
                    f"""
                    <div class="user-row">

                        <div class="user-message">

                            {safe_text}

                            <div class="user-time">
                                {datetime.now().strftime("%I:%M %p")} ✓
                            </div>

                        </div>

                        <div class="user-avatar">
                            ●
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                safe_text = message["content"].replace(
                    "<",
                    "&lt;"
                ).replace(
                    ">",
                    "&gt;"
                )

                st.markdown(
                    f"""
                    <div class="ai-row">

                        <div class="ai-avatar">
                            🤖
                        </div>

                        <div class="ai-message">

                            {safe_text}

                            <div class="ai-time">
                                {datetime.now().strftime("%I:%M %p")}
                            </div>

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
    # CHAT INPUT
    # ========================================================

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

        with st.spinner("Danish AI is thinking..."):

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

            except Exception as e:

                st.error(
                    "Danish AI could not respond. "
                    "Please check your OpenAI API key."
                )


# ============================================================
# CHAT PAGE
# ============================================================

elif st.session_state.page == "Chat":

    st.markdown(
        """
        <div class="greeting">
            AI Chat
            <span class="greeting-name">💬</span>
        </div>

        <div class="greeting-sub">
            Talk with Danish AI.
        </div>
        """,
        unsafe_allow_html=True
    )


    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        if message["role"] == "user":

            with st.chat_message("user"):
                st.markdown(message["content"])

        else:

            with st.chat_message("assistant"):
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


# ============================================================
# STATS PAGE
# ============================================================

elif st.session_state.page == "Stats":

    st.markdown(
        """
        <div class="greeting">
            Usage & Stats
            <span class="greeting-name">📊</span>
        </div>

        <div class="greeting-sub">
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
            assistant_messages
        )


# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="greeting">
            Settings
            <span class="greeting-name">⚙️</span>
        </div>

        <div class="greeting-sub">
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
        "🔥 Roast Mode"
    )


    st.info(
        "Danish AI — Your Intelligent AI Assistant"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        Danish AI • Your Intelligent AI Assistant
        <span class="footer-heart">♡</span>
    </div>
    """,
    unsafe_allow_html=True
)
