import streamlit as st
from openai import OpenAI
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
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
You are Danish AI, a friendly, intelligent and professional AI assistant.

Your job is to:
- Answer questions clearly and accurately.
- Be helpful, friendly and conversational.
- Support English and Urdu.
- Explain difficult topics in simple language when needed.
- Help with programming, AI, business, education and general questions.

ROAST MODE:
If the user asks to roast them or Roast Mode is enabled:
- Give a funny, playful and harmless roast.
- Do not use hateful, threatening or seriously abusive language.
- Keep it entertaining.
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

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "responses" not in st.session_state:
    st.session_state.responses = 0

if "roasts" not in st.session_state:
    st.session_state.roasts = 0


# ============================================================
# CALCULATE STATS
# ============================================================

user_messages = [
    m for m in st.session_state.messages
    if m["role"] == "user"
]

assistant_messages = [
    m for m in st.session_state.messages
    if m["role"] == "assistant"
]

total_messages = len(st.session_state.messages)
question_count = len(user_messages)
response_count = len(assistant_messages)
roast_count = st.session_state.roasts


# ============================================================
# CUSTOM CSS
# ============================================================

css = '''
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI",
                 sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(110, 60, 220, 0.12), transparent 28%),
        radial-gradient(circle at 80% 20%, rgba(30, 100, 220, 0.10), transparent 25%),
        #070b1d;
    color: #f5f7ff;
}


/* ============================================================
   HIDE STREAMLIT DEFAULT BRANDING
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080c20 0%,
            #090d24 55%,
            #070a19 100%
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}


/* ============================================================
   BRAND
   ============================================================ */

.brand-box {
    padding: 10px 8px 28px 8px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-logo {
    width: 58px;
    height: 58px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 31px;
    background:
        linear-gradient(
            135deg,
            #6d22ff,
            #923cff
        );
    box-shadow:
        0 0 30px rgba(123, 48, 255, 0.35);
}

.brand-name {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
}

.brand-subtitle {
    font-size: 12px;
    color: #8d94ad;
    margin-top: 3px;
}


/* ============================================================
   SIDEBAR LABELS
   ============================================================ */

.sidebar-label {
    color: #6f7794;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 10px 0 9px 7px;
}


/* ============================================================
   SIDEBAR BUTTONS
   ============================================================ */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 11px;
    border: 1px solid transparent;
    background: transparent;
    color: #c9cede;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
    padding-left: 15px;
    transition: 0.2s;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(115, 42, 255, 0.13);
    border-color: rgba(135, 75, 255, 0.22);
    color: white;
}


/* ============================================================
   PREMIUM CARD
   ============================================================ */

.premium-card {
    margin-top: 30px;
    padding: 19px;
    border-radius: 17px;
    border: 1px solid rgba(139, 66, 255, 0.35);
    background:
        linear-gradient(
            145deg,
            rgba(101, 35, 204, 0.25),
            rgba(49, 18, 105, 0.16)
        );
}

.premium-title {
    color: #d78cff;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 8px;
}

.premium-text {
    color: #9da4bb;
    font-size: 12px;
    line-height: 1.5;
    margin-bottom: 14px;
}


/* ============================================================
   USER CARD
   ============================================================ */

.user-card {
    margin-top: 25px;
    padding-top: 18px;
    border-top: 1px solid rgba(255,255,255,0.08);
}

.user-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #6325d9, #9b40ff);
    font-weight: 800;
    color: white;
    margin-right: 10px;
}

.user-name {
    color: white;
    font-size: 14px;
    font-weight: 700;
}

.user-plan {
    color: #858da8;
    font-size: 11px;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.greeting {
    font-size: 34px;
    font-weight: 800;
    line-height: 1.2;
    color: white;
}

.greeting-name {
    background:
        linear-gradient(
            90deg,
            #8a3cff,
            #6c72ff
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-subtitle {
    color: #8d95ad;
    font-size: 14px;
    margin-top: 8px;
}


/* ============================================================
   DATE CARD
   ============================================================ */

.date-card {
    min-width: 175px;
    padding: 14px 18px;
    border-radius: 16px;
    background: rgba(19, 25, 48, 0.78);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.date-icon {
    font-size: 23px;
}

.date-text {
    font-size: 13px;
    font-weight: 700;
    color: white;
}

.time-text {
    font-size: 11px;
    color: #858da7;
    margin-top: 3px;
}


/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-card {
    min-height: 195px;
    padding: 21px;
    border-radius: 20px;
    position: relative;
    overflow: hidden;
    background: rgba(14, 19, 39, 0.82);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 12px 35px rgba(0,0,0,0.16);
}

.stat-card-purple {
    border-color: rgba(157, 63, 255, 0.38);
}

.stat-card-blue {
    border-color: rgba(38, 137, 255, 0.35);
}

.stat-card-green {
    border-color: rgba(40, 220, 130, 0.32);
}

.stat-card-orange {
    border-color: rgba(255, 165, 35, 0.32);
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    margin-bottom: 17px;
}

.icon-purple {
    background: rgba(137, 46, 255, 0.18);
    color: #b44cff;
}

.icon-blue {
    background: rgba(30, 130, 255, 0.16);
    color: #43a5ff;
}

.icon-green {
    background: rgba(20, 210, 125, 0.13);
    color: #3ee893;
}

.icon-orange {
    background: rgba(255, 165, 20, 0.13);
    color: #ffad2f;
}

.stat-number {
    font-size: 29px;
    font-weight: 800;
    color: white;
}

.stat-title {
    margin-top: 5px;
    font-size: 14px;
    font-weight: 700;
    color: #d7d9e5;
}

.stat-description {
    margin-top: 5px;
    font-size: 11px;
    color: #858da8;
}


/* ============================================================
   CHAT PANEL
   ============================================================ */

.chat-panel {
    margin-top: 28px;
    min-height: 510px;
    border-radius: 21px;
    border: 1px solid rgba(255,255,255,0.09);
    background:
        linear-gradient(
            180deg,
            rgba(12, 17, 37, 0.95),
            rgba(8, 12, 28, 0.96)
        );
    overflow: hidden;
}

.chat-header {
    padding: 22px 26px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

.chat-subtitle {
    color: #8189a5;
    font-size: 12px;
    margin-top: 4px;
}


/* ============================================================
   EMPTY CHAT
   ============================================================ */

.empty-chat {
    text-align: center;
    padding: 100px 20px 75px 20px;
}

.empty-icon {
    width: 65px;
    height: 65px;
    margin: auto;
    border-radius: 21px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #5d22d5, #8d36ff);
    font-size: 31px;
    box-shadow: 0 0 35px rgba(118, 45, 255, 0.25);
}

.empty-title {
    font-size: 24px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
}

.empty-text {
    color: #8088a3;
    font-size: 13px;
    margin-top: 6px;
}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {
    background: rgba(21, 27, 51, 0.72);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p {
    color: #e9ebf4;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    padding-top: 12px;
}

[data-testid="stChatInput"] textarea {
    background: #151b32 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
    border-radius: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #727b98 !important;
}


/* ============================================================
   NORMAL BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 11px;
    border: 1px solid rgba(145, 74, 255, 0.38);
    background: rgba(106, 36, 220, 0.18);
    color: #f1ecff;
    font-weight: 700;
}

.stButton > button:hover {
    border-color: #9147ff;
    background: rgba(115, 42, 240, 0.28);
    color: white;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 23px;
    font-weight: 800;
    color: white;
    margin-top: 30px;
    margin-bottom: 15px;
}

.info-box {
    padding: 20px;
    border-radius: 17px;
    background: rgba(16, 22, 44, 0.8);
    border: 1px solid rgba(255,255,255,0.08);
    color: #aeb5ca;
}


/* ============================================================
   FOOTER
   ============================================================ */

.custom-footer {
    text-align: center;
    color: #737b97;
    font-size: 12px;
    margin-top: 28px;
    padding-bottom: 10px;
}

.custom-footer span {
    color: #a34dff;
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
        <div class="brand-box">
            <div class="brand-row">
                <div class="brand-logo">🤖</div>
                <div>
                    <div class="brand-name">Danish AI</div>
                    <div class="brand-subtitle">Your intelligent AI Assistant</div>
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

    if st.button("💬  AI Chat", use_container_width=True):
        st.session_state.page = "AI Chat"

    if st.button("📊  Usage & Stats", use_container_width=True):
        st.session_state.page = "Usage & Stats"

    if st.button("⚙️  Settings", use_container_width=True):
        st.session_state.page = "Settings"

    st.markdown(
        '<div class="sidebar-label" style="margin-top:30px;">CHAT</div>',
        unsafe_allow_html=True
    )

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = []
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

    st.button("Upgrade Now", use_container_width=True)

    st.markdown(
        '''
        <div class="user-card">
            <div>
                <span class="user-avatar">D</span>
                <span class="user-name">Danish</span>
            </div>
            <div style="margin-left:55px;margin-top:-5px;">
                <span class="user-plan">Free Plan</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT DATE / TIME
# ============================================================

now = datetime.now()

date_string = now.strftime("%B %d, %Y")
time_string = now.strftime("%I:%M %p")


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        f'''
        <div class="page-header">
            <div>
                <div class="greeting">
                    Good evening,
                    <span class="greeting-name">Danish</span> 👋
                </div>
                <div class="header-subtitle">
                    Here's what's happening with Danish AI today.
                </div>
            </div>

            <div class="date-card">
                <div class="date-icon">📅</div>
                <div class="date-text">{date_string}</div>
                <div class="time-text">{time_string}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f'''
            <div class="stat-card stat-card-purple">
                <div class="stat-icon icon-purple">💬</div>
                <div class="stat-number">{total_messages}</div>
                <div class="stat-title">Messages</div>
                <div class="stat-description">Total messages</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'''
            <div class="stat-card stat-card-blue">
                <div class="stat-icon icon-blue">❓</div>
                <div class="stat-number">{question_count}</div>
                <div class="stat-title">Questions</div>
                <div class="stat-description">Asked by you</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'''
            <div class="stat-card stat-card-green">
                <div class="stat-icon icon-green">🤖</div>
                <div class="stat-number">{response_count}</div>
                <div class="stat-title">AI Responses</div>
                <div class="stat-description">From Danish AI</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f'''
            <div class="stat-card stat-card-orange">
                <div class="stat-icon icon-orange">🔥</div>
                <div class="stat-number">{roast_count}</div>
                <div class="stat-title">Roast Mode</div>
                <div class="stat-description">Funny roasts</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # CHAT AREA
    # --------------------------------------------------------

    st.markdown(
        '''
        <div class="chat-panel">
            <div class="chat-header">
                <div>
                    <div class="chat-title">💬 AI Chat</div>
                    <div class="chat-subtitle">Talk with Danish AI.</div>
                </div>
            </div>
        ''',
        unsafe_allow_html=True
    )

    if not st.session_state.messages:

        st.markdown(
            '''
            <div class="empty-chat">
                <div class="empty-icon">🤖</div>
                <div class="empty-title">How can I help you?</div>
                <div class="empty-text">
                    Ask Danish AI anything.
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ROAST MODE
    # --------------------------------------------------------

    roast_col, new_col = st.columns([1, 5])

    with roast_col:
        roast_clicked = st.button(
            "🔥 Roast Mode",
            use_container_width=True
        )

        if roast_clicked:
            st.session_state.roast_mode = not st.session_state.roast_mode
            st.rerun()

    with new_col:
        if st.session_state.roast_mode:
            st.success("🔥 Roast Mode is ON")

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_input = st.chat_input("Type your message...")

    if user_input:

        is_roast = st.session_state.roast_mode

        if is_roast:
            final_system_prompt = SYSTEM_PROMPT + """
            
            ROAST MODE IS CURRENTLY ON.
            Respond with a funny, playful roast when appropriate.
            """
            st.session_state.roasts += 1
        else:
            final_system_prompt = SYSTEM_PROMPT

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.questions += 1

        api_messages = [
            {
                "role": "system",
                "content": final_system_prompt
            }
        ]

        api_messages.extend(st.session_state.messages)

        try:

            with st.spinner("Danish AI is thinking..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages
                )

                answer = response.choices[0].message.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.session_state.responses += 1

            st.rerun()

        except Exception as error:

            st.error(
                "Danish AI could not respond. "
                "Please check your OpenAI API key and try again."
            )

            st.code(str(error))


    # --------------------------------------------------------
    # DISPLAY MESSAGES
    # --------------------------------------------------------

    if st.session_state.messages:

        st.markdown(
            '<div class="section-title">Conversation</div>',
            unsafe_allow_html=True
        )

        for message in st.session_state.messages:

            if message["role"] == "user":

                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])

            elif message["role"] == "assistant":

                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])


# ============================================================
# AI CHAT PAGE
# ============================================================

elif st.session_state.page == "AI Chat":

    st.markdown(
        '''
        <div class="page-header">
            <div>
                <div class="greeting">
                    AI <span class="greeting-name">Chat</span> 💬
                </div>
                <div class="header-subtitle">
                    Talk directly with Danish AI.
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])

        elif message["role"] == "assistant":

            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"])

    user_input = st.chat_input("Ask Danish AI anything...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        try:

            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            api_messages.extend(st.session_state.messages)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages
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

            st.error("Something went wrong.")
            st.code(str(error))


# ============================================================
# USAGE & STATS PAGE
# ============================================================

elif st.session_state.page == "Usage & Stats":

    st.markdown(
        '''
        <div class="page-header">
            <div>
                <div class="greeting">
                    Usage <span class="greeting-name">& Stats</span> 📊
                </div>
                <div class="header-subtitle">
                    Your Danish AI activity.
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Messages", total_messages)

    with col2:
        st.metric("Questions", question_count)

    with col3:
        st.metric("AI Responses", response_count)

    st.markdown(
        '''
        <div class="info-box">
            <strong>🔥 Roast Mode</strong><br>
            Funny roast sessions: 
        ''',
        unsafe_allow_html=True
    )

    st.write(roast_count)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '''
        <div class="page-header">
            <div>
                <div class="greeting">
                    Danish AI <span class="greeting-name">Settings</span> ⚙️
                </div>
                <div class="header-subtitle">
                    Manage your assistant preferences.
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("Language")

    language = st.selectbox(
        "Choose language",
        [
            "English",
            "Urdu",
            "English + Urdu"
        ]
    )

    st.write("Roast Mode")

    roast_setting = st.toggle(
        "Enable Roast Mode",
        value=st.session_state.roast_mode
    )

    st.session_state.roast_mode = roast_setting

    st.markdown(
        '<div class="section-title">Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '''
        <div class="info-box">
            <strong>Danish</strong><br>
            Free Plan<br><br>
            Danish AI is ready to assist you.
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🗑️ Delete Conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.questions = 0
        st.session_state.responses = 0
        st.session_state.roasts = 0

        st.success("Conversation cleared.")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '''
    <div class="custom-footer">
        Danish AI · Your Intelligent AI Assistant · Made with
        <span>♥</span>
    </div>
    ''',
    unsafe_allow_html=True
)
