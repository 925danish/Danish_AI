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
# AI PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Danish AI, a friendly and intelligent AI assistant.

You can help with:
- General questions
- Python and programming
- Artificial intelligence
- Software engineering
- Business
- Freelancing
- Writing
- Learning

Speak English or Urdu depending on the user's language.

If the user asks for a roast:
Give a funny, playful and harmless roast.
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
# CSS DESIGN
# ============================================================

css = '''
<style>

/* MAIN BACKGROUND */

.stApp {
    background: #080d20;
    color: #ffffff;
}


/* REMOVE STREAMLIT BRANDING */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #080d20;
    border-right: 1px solid #202945;
}

[data-testid="stSidebar"] > div {
    padding: 22px 20px;
}


/* BRAND */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 35px;
}

.brand-logo {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 8px 30px rgba(124,58,237,0.35);
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
}

.brand-sub {
    color: #8993aa;
    font-size: 10px;
    margin-top: 3px;
}


/* SIDEBAR TITLES */

.sidebar-title {
    color: #727e97;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-top: 22px;
    margin-bottom: 8px;
}


/* SIDEBAR BUTTONS */

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 43px;
    background: transparent;
    color: #dce2ef;
    border: 1px solid transparent;
    border-radius: 10px;
    text-align: left;
    font-size: 13px;
    margin-bottom: 5px;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: #24134b;
    border-color: #6237a7;
    color: white;
}


/* PREMIUM CARD */

.premium {
    margin-top: 30px;
    padding: 17px;
    border-radius: 15px;
    background: linear-gradient(145deg, #28134f, #15152e);
    border: 1px solid #57309b;
}

.premium-title {
    color: #c084fc;
    font-size: 14px;
    font-weight: 700;
}

.premium-text {
    color: #a5aec1;
    font-size: 11px;
    line-height: 1.5;
    margin-top: 7px;
    margin-bottom: 13px;
}


/* PROFILE */

.profile {
    border-top: 1px solid #202945;
    margin-top: 30px;
    padding-top: 18px;
}

.profile-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #38206c;
    color: #d8b4fe;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-right: 8px;
}

.profile-name {
    color: white;
    font-size: 13px;
    font-weight: 600;
}

.profile-plan {
    color: #7d879d;
    font-size: 10px;
}


/* MAIN HEADING */

.heading {
    font-size: 35px;
    font-weight: 800;
    letter-spacing: -1px;
}

.heading-purple {
    color: #8b5cf6;
}

.subtitle {
    color: #8792a9;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 25px;
}


/* DATE */

.date-card {
    background: #101729;
    border: 1px solid #27314b;
    border-radius: 15px;
    padding: 13px;
    text-align: center;
}

.date-value {
    color: #e3e8f2;
    font-size: 11px;
    font-weight: 700;
    margin-top: 3px;
}

.time-value {
    color: #7b879e;
    font-size: 10px;
    margin-top: 2px;
}


/* STAT CARDS */

.stat {
    min-height: 145px;
    padding: 19px;
    border-radius: 17px;
    background: #0d1428;
}

.stat-purple {
    border: 1px solid #492775;
    background: linear-gradient(145deg, #17102e, #0d1428);
}

.stat-blue {
    border: 1px solid #193e72;
    background: linear-gradient(145deg, #0c1a32, #0d1428);
}

.stat-green {
    border: 1px solid #124d45;
    background: linear-gradient(145deg, #0a2425, #0d1428);
}

.stat-orange {
    border: 1px solid #5b401b;
    background: linear-gradient(145deg, #241b0e, #0d1428);
}

.stat-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    margin-bottom: 12px;
}

.icon-purple {
    background: #29104e;
}

.icon-blue {
    background: #102e55;
}

.icon-green {
    background: #0b3831;
}

.icon-orange {
    background: #493016;
}

.stat-number {
    font-size: 27px;
    font-weight: 800;
}

.stat-name {
    font-size: 13px;
    font-weight: 700;
    margin-top: 2px;
}

.stat-description {
    color: #7e899f;
    font-size: 10px;
    margin-top: 4px;
}


/* CHAT HEADER */

.chat-header {
    margin-top: 28px;
    padding: 20px 23px;
    background: #0a1022;
    border: 1px solid #242e48;
    border-radius: 18px 18px 0 0;
}

.chat-title {
    font-size: 21px;
    font-weight: 800;
}

.chat-description {
    color: #7e899f;
    font-size: 12px;
    margin-top: 3px;
}


/* WELCOME */

.welcome {
    text-align: center;
    padding: 45px 10px 35px;
}

.welcome-icon {
    font-size: 50px;
}

.welcome-title {
    font-size: 28px;
    font-weight: 800;
    margin-top: 10px;
}

.welcome-text {
    color: #7e899f;
    font-size: 12px;
    margin-top: 6px;
}


/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    border-radius: 15px;
    background: #11192c;
    border: 1px solid #26314a;
    margin-bottom: 10px;
}


/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: #1a2337;
    border: 1px solid #3a465f;
    border-radius: 16px;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #77839a !important;
}


/* NORMAL BUTTONS */

.stButton button {
    background: #11192b;
    color: #e5e7eb;
    border: 1px solid #29344c;
    border-radius: 10px;
    font-weight: 600;
}

.stButton button:hover {
    background: #25154a;
    border-color: #7c3aed;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #69758d;
    font-size: 10px;
    padding: 20px 0;
}

</style>
'''

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '''
        <div class="brand">
            <div class="brand-logo">🤖</div>

            <div>
                <div class="brand-name">Danish AI</div>
                <div class="brand-sub">
                    Your intelligent AI Assistant
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-title">WORKSPACE</div>',
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
        '<div class="sidebar-title">CHAT</div>',
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

    st.markdown(
        '''
        <div class="premium">

            <div class="premium-title">
                👑 Danish AI Premium
            </div>

            <div class="premium-text">
                Unlock more power and exclusive features.
            </div>

        </div>
        ''',
        unsafe_allow_html=True
    )

    if st.button("✨   Upgrade Now"):
        st.info("Premium plans coming soon.")

    st.markdown(
        '''
        <div class="profile">

            <span class="profile-circle">D</span>

            <span>
                <span class="profile-name">Danish</span><br>
                <span class="profile-plan">Free Plan</span>
            </span>

        </div>
        ''',
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

    left, right = st.columns([5, 1.15])

    with left:

        st.markdown(
            '''
            <div class="heading">
                Good evening,
                <span class="heading-purple">Danish</span>
                👋
            </div>

            <div class="subtitle">
                Here's what's happening with Danish AI today.
            </div>
            ''',
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            f'''
            <div class="date-card">
                📅
                <div class="date-value">{date_text}</div>
                <div class="time-value">{time_text}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )


    # STATISTICS

    user_count = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "user"
        ]
    )

    ai_count = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "assistant"
        ]
    )

    total_count = user_count + ai_count


    # CARDS

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f'''
            <div class="stat stat-purple">

                <div class="stat-icon icon-purple">
                    💬
                </div>

                <div class="stat-number">
                    {total_count}
                </div>

                <div class="stat-name">
                    Messages
                </div>

                <div class="stat-description">
                    Total messages
                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f'''
            <div class="stat stat-blue">

                <div class="stat-icon icon-blue">
                    👤
                </div>

                <div class="stat-number">
                    {user_count}
                </div>

                <div class="stat-name">
                    Questions
                </div>

                <div class="stat-description">
                    Asked by you
                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f'''
            <div class="stat stat-green">

                <div class="stat-icon icon-green">
                    🤖
                </div>

                <div class="stat-number">
                    {ai_count}
                </div>

                <div class="stat-name">
                    AI Responses
                </div>

                <div class="stat-description">
                    From Danish AI
                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            '''
            <div class="stat stat-orange">

                <div class="stat-icon icon-orange">
                    🔥
                </div>

                <div class="stat-number">
                    0
                </div>

                <div class="stat-name">
                    Roast Mode
                </div>

                <div class="stat-description">
                    Funny roasts
                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )


    # CHAT HEADER

    st.markdown(
        '''
        <div class="chat-header">

            <div class="chat-title">
                💬 AI Chat
            </div>

            <div class="chat-description">
                Talk with Danish AI.
            </div>

        </div>
        ''',
        unsafe_allow_html=True
    )


    # NEW CHAT

    if st.button("➕   New Chat"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()


    # WELCOME

    if len(st.session_state.messages) == 1:

        st.markdown(
            '''
            <div class="welcome">

                <div class="welcome-icon">
                    🤖
                </div>

                <div class="welcome-title">
                    How can I help you today?
                </div>

                <div class="welcome-text">
                    Ask Danish AI anything.
                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )


    # EXISTING MESSAGES

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # CHAT INPUT

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

            with st.spinner(
                "Danish AI is thinking..."
            ):

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

                except Exception as error:

                    st.error(
                        "Danish AI couldn't respond. "
                        "Please try again."
                    )


# ============================================================
# AI CHAT PAGE
# ============================================================

elif st.session_state.page == "Chat":

    st.markdown(
        '''
        <div class="heading">
            AI Chat
            <span class="heading-purple">💬</span>
        </div>

        <div class="subtitle">
            Talk with Danish AI.
        </div>
        ''',
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

            with st.spinner(
                "Danish AI is thinking..."
            ):

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

                except Exception:

                    st.error(
                        "Danish AI couldn't respond."
                    )


# ============================================================
# USAGE & STATS
# ============================================================

elif st.session_state.page == "Stats":

    st.markdown(
        '''
        <div class="heading">
            Usage & Stats
            <span class="heading-purple">📊</span>
        </div>

        <div class="subtitle">
            Your Danish AI activity.
        </div>
        ''',
        unsafe_allow_html=True
    )


    user_count = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "user"
        ]
    )

    ai_count = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "assistant"
        ]
    )

    total_count = user_count + ai_count


    a, b, c = st.columns(3)

    with a:
        st.metric("Questions", user_count)

    with b:
        st.metric("AI Responses", ai_count)

    with c:
        st.metric("Total Messages", total_count)


# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '''
        <div class="heading">
            Settings
            <span class="heading-purple">⚙️</span>
        </div>

        <div class="subtitle">
            Customize your Danish AI experience.
        </div>
        ''',
        unsafe_allow_html=True
    )


    st.subheader("Preferences")

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
            "Danish Dark"
        ]
    )


    st.subheader("AI Features")

    st.toggle(
        "🔥 Roast Mode"
    )


    st.subheader("About")

    st.info(
        "Danish AI — Your Intelligent AI Assistant"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '''
    <div class="footer">
        Danish AI • Your Intelligent AI Assistant ♡
    </div>
    ''',
    unsafe_allow_html=True
)
