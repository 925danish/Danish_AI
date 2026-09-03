import streamlit as st
from openai import OpenAI

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

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "AI Chat"

if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False

# ============================================================
# PROMPTS
# ============================================================

NORMAL_PROMPT = (
    "You are Danish AI, a professional, friendly and intelligent AI assistant. "
    "Answer clearly, accurately and naturally. "
    "You can communicate in English or Urdu. "
    "Be helpful, conversational and concise when appropriate."
)

ROAST_PROMPT = (
    "You are Danish AI Roast Mode. "
    "Give funny, playful and harmless roasts. "
    "Keep everything entertaining and friendly. "
    "Never use hateful, threatening or seriously abusive language."
)

# ============================================================
# PROFESSIONAL DESIGN
# ============================================================

css = (
    "<style>"
    
    ".stApp{"
    "background:#070914;"
    "color:#f5f7ff;"
    "}"
    
    "[data-testid='stSidebar']{"
    "background:#090d1f;"
    "border-right:1px solid #202743;"
    "}"
    
    "[data-testid='stSidebar'] *{"
    "color:#f3f4ff;"
    "}"
    
    ".brand{"
    "font-size:30px;"
    "font-weight:800;"
    "letter-spacing:-1px;"
    "margin-top:8px;"
    "}"
    
    ".brand-ai{"
    "color:#8b5cf6;"
    "}"
    
    ".tagline{"
    "color:#7f89aa;"
    "font-size:13px;"
    "margin-top:5px;"
    "margin-bottom:25px;"
    "}"
    
    ".hero{"
    "background:linear-gradient(135deg,#101630,#17113b);"
    "border:1px solid #292d5b;"
    "border-radius:24px;"
    "padding:32px;"
    "margin-bottom:22px;"
    "box-shadow:0 15px 45px rgba(0,0,0,.25);"
    "}"
    
    ".hero-title{"
    "font-size:34px;"
    "font-weight:800;"
    "margin:0;"
    "}"
    
    ".gradient-text{"
    "background:linear-gradient(90deg,#8b5cf6,#4f8cff);"
    "-webkit-background-clip:text;"
    "-webkit-text-fill-color:transparent;"
    "}"
    
    ".hero-text{"
    "color:#9aa4c6;"
    "font-size:15px;"
    "margin-top:10px;"
    "line-height:1.6;"
    "}"
    
    ".card{"
    "background:#0d1227;"
    "border:1px solid #202743;"
    "border-radius:20px;"
    "padding:22px;"
    "min-height:120px;"
    "}"
    
    ".card-label{"
    "color:#858eae;"
    "font-size:13px;"
    "}"
    
    ".card-number{"
    "font-size:30px;"
    "font-weight:800;"
    "margin-top:8px;"
    "}"
    
    ".welcome-card{"
    "background:#0d1227;"
    "border:1px solid #22294a;"
    "border-radius:22px;"
    "padding:28px;"
    "margin-top:18px;"
    "}"
    
    ".welcome-title{"
    "font-size:24px;"
    "font-weight:800;"
    "}"
    
    ".welcome-text{"
    "color:#919abb;"
    "margin-top:8px;"
    "line-height:1.6;"
    "}"
    
    ".pro-card{"
    "background:linear-gradient(135deg,#7c3aed,#4f46e5);"
    "border-radius:18px;"
    "padding:20px;"
    "margin-top:25px;"
    "}"
    
    ".pro-title{"
    "font-size:19px;"
    "font-weight:800;"
    "}"
    
    ".pro-text{"
    "font-size:13px;"
    "margin-top:6px;"
    "color:#ddd6fe;"
    "}"
    
    ".section-title{"
    "font-size:24px;"
    "font-weight:800;"
    "margin-bottom:12px;"
    "}"
    
    ".status{"
    "display:inline-block;"
    "padding:6px 12px;"
    "border-radius:20px;"
    "background:#172554;"
    "color:#93c5fd;"
    "font-size:12px;"
    "}"
    
    ".roast-banner{"
    "background:linear-gradient(135deg,#3b0764,#701a75);"
    "border:1px solid #a855f7;"
    "border-radius:18px;"
    "padding:18px;"
    "margin-bottom:20px;"
    "}"
    
    ".footer{"
    "text-align:center;"
    "color:#59627f;"
    "font-size:12px;"
    "padding:30px 0;"
    "}"
    
    ".stButton>button{"
    "border-radius:12px;"
    "border:1px solid #292f52;"
    "background:#11172d;"
    "color:#ffffff;"
    "font-weight:600;"
    "}"
    
    ".stButton>button:hover{"
    "border-color:#8b5cf6;"
    "color:#ffffff;"
    "}"
    
    "</style>"
)

st.markdown(css, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "<div class='brand'>Danish <span class='brand-ai'>AI</span></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='tagline'>Your intelligent AI assistant</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "AI Chat",
            "Dashboard",
            "Roast Mode",
            "Settings"
        ],
        index=[
            "AI Chat",
            "Dashboard",
            "Roast Mode",
            "Settings"
        ].index(st.session_state.page),
        label_visibility="collapsed"
    )

    st.session_state.page = page

    st.markdown("---")

    st.markdown(
        "<div class='pro-card'>"
        "<div class='pro-title'>👑 Danish AI Pro</div>"
        "<div class='pro-text'>Unlock the full AI experience.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# AI CHAT
# ============================================================

if st.session_state.page == "AI Chat":

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>Welcome to <span class='gradient-text'>Danish AI</span> 🤖</div>"
        "<div class='hero-text'>"
        "Your personal AI assistant for questions, ideas, coding, learning and more."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.messages:

        st.markdown(
            "<div class='welcome-card'>"
            "<div class='welcome-title'>How can I help you today?</div>"
            "<div class='welcome-text'>"
            "Ask me anything. I can help with Python, AI, software engineering, "
            "business ideas, writing, learning and everyday questions."
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Message Danish AI...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.total_messages += 1

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            if client is None:

                answer = (
                    "⚠️ OpenAI is not connected. "
                    "Please check your OPENAI_API_KEY in Streamlit Secrets."
                )

            else:

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": NORMAL_PROMPT
                            }
                        ]
                        + st.session_state.messages
                    )

                    answer = response.choices[0].message.content

                except Exception as error:

                    answer = (
                        "⚠️ Something went wrong while contacting the AI.\n\n"
                        + str(error)
                    )

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

# ============================================================
# DASHBOARD
# ============================================================

elif st.session_state.page == "Dashboard":

    st.markdown(
        "<div class='section-title'>📊 Dashboard</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='hero'>"
        "<div class='hero-title'>Danish AI Overview</div>"
        "<div class='hero-text'>"
        "Track your conversation activity and AI usage."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "<div class='card'>"
            "<div class='card-label'>Total Messages</div>"
            "<div class='card-number'>"
            + str(st.session_state.total_messages)
            + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            "<div class='card'>"
            "<div class='card-label'>Current Chats</div>"
            "<div class='card-number'>"
            + str(len(st.session_state.messages))
            + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    with col3:

        status = "Connected" if client is not None else "Not Connected"

        st.markdown(
            "<div class='card'>"
            "<div class='card-label'>AI Status</div>"
            "<div class='card-number'>"
            + status
            + "</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("")

    st.info(
        "💡 Your dashboard is currently session-based. "
        "Later we can add user accounts, permanent usage statistics and analytics."
    )

# ============================================================
# ROAST MODE
# ============================================================

elif st.session_state.page == "Roast Mode":

    st.markdown(
        "<div class='roast-banner'>"
        "<div class='hero-title'>🔥 Roast Mode</div>"
        "<div class='hero-text'>"
        "Ready for some playful AI roasting?"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.warning(
        "Roast Mode is designed for funny and harmless jokes."
    )

    roast_input = st.chat_input("Give me something to roast...")

    if roast_input:

        with st.chat_message("user"):
            st.markdown(roast_input)

        if client is None:

            roast_answer = (
                "⚠️ OpenAI is not connected. "
                "Please check your API key."
            )

        else:

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": ROAST_PROMPT
                        },
                        {
                            "role": "user",
                            "content": roast_input
                        }
                    ]
                )

                roast_answer = response.choices[0].message.content

            except Exception as error:

                roast_answer = "⚠️ Error: " + str(error)

        with st.chat_message("assistant"):
            st.markdown(roast_answer)

# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        "<div class='section-title'>⚙️ Settings</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='welcome-card'>"
        "<div class='welcome-title'>Danish AI Settings</div>"
        "<div class='welcome-text'>"
        "Manage your AI experience."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("")

    st.checkbox(
        "Enable Roast Mode",
        value=st.session_state.roast_mode,
        key="roast_setting"
    )

    st.session_state.roast_mode = st.session_state.roast_setting

    st.markdown("### AI Information")

    st.write("**Assistant:** Danish AI")
    st.write("**Model:** GPT-4o-mini")
    st.write(
        "**API Status:** "
        + ("Connected ✅" if client is not None else "Not connected ⚠️")
    )

    st.markdown("### Conversation")

    if st.button("Clear all messages", use_container_width=True):

        st.session_state.messages = []
        st.session_state.total_messages = 0

        st.success("Conversation cleared.")
        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<div class='footer'>"
    "Danish AI • Built with Python, Streamlit & OpenAI"
    "</div>",
    unsafe_allow_html=True
)
