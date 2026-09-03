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

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# ============================================================
# AI INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = (
    "You are Danish AI, a friendly and intelligent AI assistant. "
    "Answer questions clearly and helpfully. "
    "You can speak English or Urdu depending on the user's language. "
    "If the user asks to roast them, give a funny, playful and harmless roast. "
    "Never use hateful, threatening or seriously abusive language."
)


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

user_messages = 0
ai_messages = 0

for message in st.session_state.messages:
    if message["role"] == "user":
        user_messages += 1
    elif message["role"] == "assistant":
        ai_messages += 1

total_messages = user_messages + ai_messages


# ============================================================
# CUSTOM CSS
# NO TRIPLE QUOTES USED
# ============================================================

css = (
    "<style>"
    
    "* { box-sizing: border-box; }"

    ".stApp {"
    "background: #070b1c;"
    "color: #ffffff;"
    "}"

    ".main .block-container {"
    "max-width: 1500px;"
    "padding-top: 32px;"
    "padding-left: 34px;"
    "padding-right: 34px;"
    "padding-bottom: 30px;"
    "}"

    "#MainMenu { visibility: hidden; }"
    "footer { visibility: hidden; }"
    "[data-testid='stToolbar'] { visibility: hidden; }"
    "[data-testid='stDecoration'] { display: none; }"

    "header {"
    "background: transparent !important;"
    "}"

    # SIDEBAR
    "[data-testid='stSidebar'] {"
    "background: #080d20;"
    "border-right: 1px solid #202943;"
    "}"

    "[data-testid='stSidebar'] > div {"
    "padding: 25px 20px;"
    "}"

    ".brand {"
    "display: flex;"
    "align-items: center;"
    "gap: 12px;"
    "margin-bottom: 34px;"
    "}"

    ".brand-logo {"
    "width: 52px;"
    "height: 52px;"
    "border-radius: 16px;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "font-size: 27px;"
    "background: linear-gradient(135deg,#9b45ff,#5d21d6);"
    "box-shadow: 0 0 25px rgba(132,48,255,.35);"
    "}"

    ".brand-title {"
    "font-size: 21px;"
    "font-weight: 800;"
    "color: #f5f3ff;"
    "}"

    ".brand-subtitle {"
    "font-size: 10px;"
    "color: #818ba1;"
    "margin-top: 4px;"
    "}"

    ".side-heading {"
    "font-size: 10px;"
    "font-weight: 800;"
    "letter-spacing: 1.5px;"
    "color: #68738b;"
    "margin-bottom: 8px;"
    "}"

    "[data-testid='stSidebar'] .stButton {"
    "margin-bottom: 5px;"
    "}"

    "[data-testid='stSidebar'] .stButton button {"
    "height: 43px;"
    "border-radius: 10px;"
    "background: transparent;"
    "border: 1px solid transparent;"
    "color: #cbd1df;"
    "font-size: 13px;"
    "font-weight: 600;"
    "}"

    "[data-testid='stSidebar'] .stButton button:hover {"
    "background: #261044;"
    "border-color: #6330a2;"
    "color: white;"
    "}"

    ".side-line {"
    "height: 1px;"
    "background: #202943;"
    "margin: 22px 0 18px 0;"
    "}"

    ".premium {"
    "margin-top: 35px;"
    "padding: 17px;"
    "border-radius: 15px;"
    "background: linear-gradient(145deg,#291448,#131126);"
    "border: 1px solid #54288c;"
    "}"

    ".premium-title {"
    "font-size: 14px;"
    "font-weight: 800;"
    "color: #b65aff;"
    "}"

    ".premium-text {"
    "font-size: 11px;"
    "line-height: 1.5;"
    "color: #929bb0;"
    "margin-top: 7px;"
    "margin-bottom: 13px;"
    "}"

    ".profile {"
    "border-top: 1px solid #202943;"
    "margin-top: 27px;"
    "padding-top: 18px;"
    "display: flex;"
    "align-items: center;"
    "}"

    ".avatar {"
    "width: 41px;"
    "height: 41px;"
    "border-radius: 50%;"
    "background: #351761;"
    "color: #bd7cff;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "font-weight: 800;"
    "margin-right: 11px;"
    "}"

    ".profile-name {"
    "font-size: 13px;"
    "font-weight: 700;"
    "color: #f0f2f7;"
    "}"

    ".profile-plan {"
    "font-size: 10px;"
    "color: #788298;"
    "margin-top: 3px;"
    "}"

    # HEADER
    ".greeting {"
    "font-size: 34px;"
    "font-weight: 800;"
    "letter-spacing: -1px;"
    "color: #f5f5f8;"
    "}"

    ".purple {"
    "color: #8746ff;"
    "}"

    ".subtitle {"
    "font-size: 12px;"
    "color: #7f899f;"
    "margin-top: 7px;"
    "margin-bottom: 27px;"
    "}"

    ".date-box {"
    "height: 78px;"
    "width: 165px;"
    "border-radius: 16px;"
    "background: #101629;"
    "border: 1px solid #29334b;"
    "padding: 12px 15px;"
    "}"

    ".date-value {"
    "font-size: 11px;"
    "font-weight: 700;"
    "color: #e7eaf1;"
    "}"

    ".time-value {"
    "font-size: 10px;"
    "color: #788298;"
    "margin-top: 3px;"
    "}"

    # STAT CARDS
    ".stat-card {"
    "height: 185px;"
    "padding: 20px;"
    "border-radius: 18px;"
    "}"

    ".purple-card {"
    "background: linear-gradient(145deg,#171029,#0c1223);"
    "border: 1px solid #542b85;"
    "}"

    ".blue-card {"
    "background: linear-gradient(145deg,#0d1b32,#0c1325);"
    "border: 1px solid #1d4d83;"
    "}"

    ".green-card {"
    "background: linear-gradient(145deg,#092421,#0c1525);"
    "border: 1px solid #155c4d;"
    "}"

    ".orange-card {"
    "background: linear-gradient(145deg,#21180d,#0d1424);"
    "border: 1px solid #67491e;"
    "}"

    ".stat-icon {"
    "width: 43px;"
    "height: 43px;"
    "border-radius: 13px;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "font-size: 20px;"
    "margin-bottom: 14px;"
    "}"

    ".purple-icon {"
    "background: #341454;"
    "border: 1px solid #7136a5;"
    "}"

    ".blue-icon {"
    "background: #102f56;"
    "border: 1px solid #205b9a;"
    "}"

    ".green-icon {"
    "background: #0a3b32;"
    "border: 1px solid #17725d;"
    "}"

    ".orange-icon {"
    "background: #493013;"
    "border: 1px solid #7a531d;"
    "}"

    ".stat-number {"
    "font-size: 28px;"
    "font-weight: 800;"
    "color: #f0f3f8;"
    "}"

    ".stat-title {"
    "font-size: 14px;"
    "font-weight: 700;"
    "color: #d8dce5;"
    "margin-top: 4px;"
    "}"

    ".stat-description {"
    "font-size: 10px;"
    "color: #7d879c;"
    "margin-top: 3px;"
    "}"

    # CHAT
    ".chat-box {"
    "margin-top: 30px;"
    "border: 1px solid #242e48;"
    "border-radius: 19px;"
    "background: #080e20;"
    "overflow: hidden;"
    "}"

    ".chat-header {"
    "padding: 20px 25px;"
    "border-bottom: 1px solid #222b42;"
    "display: flex;"
    "align-items: center;"
    "gap: 13px;"
    "}"

    ".chat-icon {"
    "width: 40px;"
    "height: 40px;"
    "border-radius: 12px;"
    "background: #351460;"
    "border: 1px solid #7034aa;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "}"

    ".chat-title {"
    "font-size: 20px;"
    "font-weight: 800;"
    "color: #f2f3f7;"
    "}"

    ".chat-subtitle {"
    "font-size: 11px;"
    "color: #7d879d;"
    "margin-top: 3px;"
    "}"

    ".empty-state {"
    "height: 360px;"
    "display: flex;"
    "flex-direction: column;"
    "align-items: center;"
    "justify-content: center;"
    "text-align: center;"
    "}"

    ".empty-logo {"
    "width: 64px;"
    "height: 64px;"
    "border-radius: 20px;"
    "background: #151d31;"
    "border: 1px solid #303b55;"
    "display: flex;"
    "align-items: center;"
    "justify-content: center;"
    "font-size: 30px;"
    "margin-bottom: 15px;"
    "}"

    ".empty-title {"
    "font-size: 25px;"
    "font-weight: 800;"
    "color: #eef0f5;"
    "}"

    ".empty-text {"
    "font-size: 11px;"
    "color: #778298;"
    "margin-top: 6px;"
    "}"

    # CHAT INPUT
    "[data-testid='stChatInput'] > div {"
    "background: #1a2336 !important;"
    "border: 1px solid #3a465f !important;"
    "border-radius: 17px !important;"
    "}"

    "[data-testid='stChatInput'] textarea {"
    "color: white !important;"
    "}"

    "[data-testid='stChatInput'] textarea::placeholder {"
    "color: #7d879c !important;"
    "}"

    # FOOTER
    ".footer {"
    "text-align: center;"
    "font-size: 10px;"
    "color: #707b91;"
    "margin-top: 22px;"
    "}"

    "</style>"
)

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<div class='brand'>"
        "<div class='brand-logo'>🤖</div>"
        "<div>"
        "<div class='brand-title'>Danish AI</div>"
        "<div class='brand-subtitle'>Your intelligent AI Assistant</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='side-heading'>WORKSPACE</div>",
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
        "<div class='side-line'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='side-heading'>CHAT</div>",
        unsafe_allow_html=True
    )

    if st.button("🗑   Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()

    st.markdown(
        "<div class='premium'>"
        "<div class='premium-title'>♛ Danish AI Premium</div>"
        "<div class='premium-text'>"
        "Unlock more power and exclusive features."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("Upgrade Now", use_container_width=True):
        st.info("Premium features coming soon.")

    st.markdown(
        "<div class='profile'>"
        "<div class='avatar'>D</div>"
        "<div>"
        "<div class='profile-name'>Danish</div>"
        "<div class='profile-plan'>Free Plan</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    left, right = st.columns([5, 1])

    with left:
        st.markdown(
            "<div class='greeting'>"
            "Good evening, "
            "<span class='purple'>Danish</span> 👋"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='subtitle'>"
            "Here's what's happening with Danish AI today."
            "</div>",
            unsafe_allow_html=True
        )

    with right:
        now = datetime.now()

        st.markdown(
            "<div class='date-box'>"
            "<div>📅</div>"
            "<div class='date-value'>"
            + now.strftime("%B %d, %Y")
            + "</div>"
            "<div class='time-value'>"
            + now.strftime("%I:%M %p")
            + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            "<div class='stat-card purple-card'>"
            "<div class='stat-icon purple-icon'>💬</div>"
            "<div class='stat-number'>"
            + str(total_messages)
            + "</div>"
            "<div class='stat-title'>Messages</div>"
            "<div class='stat-description'>Total messages</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            "<div class='stat-card blue-card'>"
            "<div class='stat-icon blue-icon'>♙</div>"
            "<div class='stat-number'>"
            + str(user_messages)
            + "</div>"
            "<div class='stat-title'>Questions</div>"
            "<div class='stat-description'>Asked by you</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            "<div class='stat-card green-card'>"
            "<div class='stat-icon green-icon'>🤖</div>"
            "<div class='stat-number'>"
            + str(ai_messages)
            + "</div>"
            "<div class='stat-title'>AI Responses</div>"
            "<div class='stat-description'>From Danish AI</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            "<div class='stat-card orange-card'>"
            "<div class='stat-icon orange-icon'>🔥</div>"
            "<div class='stat-number'>0</div>"
            "<div class='stat-title'>Roast Mode</div>"
            "<div class='stat-description'>Funny roasts</div>"
            "</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # CHAT HEADER
    # --------------------------------------------------------

    st.markdown(
        "<div class='chat-box'>"
        "<div class='chat-header'>"
        "<div class='chat-icon'>💬</div>"
        "<div>"
        "<div class='chat-title'>AI Chat</div>"
        "<div class='chat-subtitle'>Talk with Danish AI.</div>"
        "</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # MESSAGES
    # --------------------------------------------------------

    visible = []

    for message in st.session_state.messages:
        if message["role"] != "system":
            visible.append(message)

    if len(visible) == 0:

        st.markdown(
            "<div class='empty-state'>"
            "<div class='empty-logo'>🤖</div>"
            "<div class='empty-title'>How can I help you?</div>"
            "<div class='empty-text'>Ask Danish AI anything.</div>"
            "</div>",
            unsafe_allow_html=True
        )

    else:

        for message in visible:

            if message["role"] == "user":
                avatar = "D"
            else:
                avatar = "🤖"

            with st.chat_message(
                message["role"],
                avatar=avatar
            ):
                st.markdown(message["content"])

    # --------------------------------------------------------
    # ROAST MODE
    # --------------------------------------------------------

    if st.button(
        "🔥 Roast Mode",
        use_container_width=False
    ):
        st.session_state.roast_mode = not st.session_state.roast_mode
        st.rerun()

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    if st.session_state.roast_mode:
        placeholder = "Roast me..."
    else:
        placeholder = "Type your message..."

    user_input = st.chat_input(placeholder)

    if user_input:

        if st.session_state.roast_mode:

            actual_message = (
                "Give me a funny, playful and harmless roast. "
                "Do not be hateful or seriously abusive. "
                "The user says: "
                + user_input
            )

        else:
            actual_message = user_input

        st.session_state.messages.append(
            {
                "role": "user",
                "content": actual_message
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

        except Exception as error:

            st.error(
                "Danish AI could not connect to OpenAI. "
                "Please check your API key."
            )


# ============================================================
# AI CHAT
# ============================================================

elif st.session_state.page == "Chat":

    st.markdown(
        "<div class='greeting'>"
        "AI Chat <span class='purple'>💬</span>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Talk with Danish AI.</div>",
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        avatar = "D" if message["role"] == "user" else "🤖"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")

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

            st.error("Danish AI could not connect to OpenAI.")


# ============================================================
# USAGE & STATS
# ============================================================

elif st.session_state.page == "Stats":

    st.markdown(
        "<div class='greeting'>"
        "Usage & Stats <span class='purple'>📊</span>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Your Danish AI activity.</div>",
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.metric("Messages", total_messages)

    with b:
        st.metric("Questions", user_messages)

    with c:
        st.metric("AI Responses", ai_messages)


# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        "<div class='greeting'>"
        "Settings <span class='purple'>⚙️</span>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>"
        "Customize your Danish AI experience."
        "</div>",
        unsafe_allow_html=True
    )

    st.selectbox(
        "Language",
        ["Automatic", "English", "Urdu"]
    )

    st.selectbox(
        "Theme",
        ["Danish AI Dark"]
    )

    st.toggle(
        "Enable Roast Mode"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<div class='footer'>"
    "Danish AI • Your Intelligent AI Assistant "
    "<span class='purple'>♡</span>"
    "</div>",
    unsafe_allow_html=True
)
