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
    st.session_state.page = "Dashboard"

if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

if "ai_responses" not in st.session_state:
    st.session_state.ai_responses = 0

if "roast_count" not in st.session_state:
    st.session_state.roast_count = 0

if "roast_mode" not in st.session_state:
    st.session_state.roast_mode = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Danish"

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
# STYLE
# ============================================================

css = """
<style>
.stApp{background:#070914;color:#f5f7ff;}
[data-testid="stSidebar"]{background:#090d1f;border-right:1px solid #202743;}
[data-testid="stSidebar"] *{color:#f3f4ff;}
#MainMenu, footer, header{visibility:hidden;}

.brand-row{display:flex;align-items:center;gap:10px;margin-top:4px;margin-bottom:2px;}
.brand-logo{
    width:40px;height:40px;border-radius:12px;
    background:linear-gradient(135deg,#8b5cf6,#4f46e5);
    display:flex;align-items:center;justify-content:center;font-size:20px;
}
.brand{font-size:22px;font-weight:800;letter-spacing:-0.5px;line-height:1.1;}
.tagline{color:#7f89aa;font-size:12px;margin-top:0px;margin-bottom:22px;}

.nav-label{color:#5b6488;font-size:11px;letter-spacing:1px;margin:18px 0 6px 4px;}

.pro-card{
    background:linear-gradient(135deg,#7c3aed,#4f46e5);
    border-radius:16px;padding:18px;margin-top:18px;
}
.pro-title{font-size:16px;font-weight:800;display:flex;align-items:center;gap:6px;}
.pro-text{font-size:12.5px;margin-top:6px;color:#ddd6fe;line-height:1.4;}

.profile-row{
    display:flex;align-items:center;gap:10px;
    border-top:1px solid #202743;padding-top:14px;margin-top:14px;
}
.profile-avatar{
    width:36px;height:36px;border-radius:50%;
    background:linear-gradient(135deg,#8b5cf6,#4f46e5);
    display:flex;align-items:center;justify-content:center;font-weight:800;
}
.profile-name{font-size:14px;font-weight:700;}
.profile-plan{font-size:11.5px;color:#7f89aa;}

.greeting-row{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:22px;flex-wrap:wrap;gap:12px;}
.greeting-title{font-size:30px;font-weight:800;margin:0;}
.greeting-accent{color:#8b5cf6;}
.greeting-sub{color:#8892b0;font-size:14.5px;margin-top:4px;}
.date-card{
    background:#0d1227;border:1px solid #202743;border-radius:16px;
    padding:12px 18px;font-size:13px;color:#c9cfe8;min-width:150px;text-align:right;
}
.date-card .time{font-size:16px;font-weight:800;color:#f5f7ff;}

.stat-card{
    background:#0d1227;border:1px solid #202743;border-radius:20px;
    padding:20px;min-height:150px;position:relative;
}
.stat-icon{
    width:40px;height:40px;border-radius:12px;
    display:flex;align-items:center;justify-content:center;font-size:19px;margin-bottom:14px;
}
.stat-number{font-size:28px;font-weight:800;margin:2px 0 2px 0;}
.stat-label{font-size:14px;font-weight:700;color:#e5e8f7;}
.stat-sub{font-size:12px;color:#7f89aa;margin-top:1px;}

.chat-panel{
    background:#0d1227;border:1px solid #202743;border-radius:22px;
    padding:22px;margin-top:24px;
}
.chat-panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:10px;}
.chat-panel-title{display:flex;align-items:center;gap:12px;}
.chat-icon-badge{
    width:38px;height:38px;border-radius:11px;background:#1b2247;
    display:flex;align-items:center;justify-content:center;font-size:18px;
}
.chat-title-text{font-size:19px;font-weight:800;}
.chat-sub-text{font-size:12.5px;color:#7f89aa;margin-top:1px;}

.msg-row{display:flex;gap:10px;margin-bottom:16px;align-items:flex-end;}
.msg-row.user{flex-direction:row-reverse;}
.avatar{
    width:34px;height:34px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;font-size:16px;
}
.avatar.user{background:#3b2f7a;}
.avatar.bot{background:#1e2a5e;}
.bubble{
    max-width:65%;padding:12px 16px;border-radius:16px;font-size:14.5px;line-height:1.5;
}
.bubble.user{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;border-bottom-right-radius:4px;}
.bubble.bot{background:#151b38;color:#f0f2fb;border-bottom-left-radius:4px;}
.msg-time{font-size:10.5px;color:#8892b0;margin-top:5px;}
.bubble.user + .msg-time, .msg-row.user .msg-time{text-align:right;}

.welcome-card{background:#101731;border:1px solid #22294a;border-radius:18px;padding:22px;margin-bottom:16px;}
.welcome-title{font-size:18px;font-weight:800;}
.welcome-text{color:#919abb;margin-top:6px;line-height:1.5;font-size:13.5px;}

.section-title{font-size:26px;font-weight:800;margin-bottom:16px;}
.footer-note{text-align:center;color:#4c5578;font-size:12px;padding:26px 0 6px 0;}

.stButton>button{
    border-radius:12px;border:1px solid #292f52;background:#11172d;
    color:#ffffff;font-weight:600;
}
.stButton>button:hover{border-color:#8b5cf6;color:#ffffff;}
div[data-testid="stChatInput"]{border-top:1px solid #202743;padding-top:12px;}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


def sparkline(color, points):
    """Inline SVG sparkline, styled like the wavy lines in the reference dashboard."""
    w, h = 220, 40
    step = w / (len(points) - 1)
    coords = " ".join(f"{i*step:.1f},{h - p*h:.1f}" for i, p in enumerate(points))
    return (
        f'<svg width="100%" height="40" viewBox="0 0 {w} {h}" '
        f'preserveAspectRatio="none" style="margin-top:10px;">'
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


SPARK_PURPLE = [0.3, 0.55, 0.35, 0.7, 0.5, 0.8, 0.6]
SPARK_BLUE = [0.4, 0.3, 0.6, 0.4, 0.65, 0.45, 0.55]
SPARK_GREEN = [0.5, 0.65, 0.4, 0.6, 0.75, 0.55, 0.7]
SPARK_ORANGE = [0.35, 0.6, 0.3, 0.55, 0.4, 0.65, 0.5]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        "<div class='brand-row'>"
        "<div class='brand-logo'>🤖</div>"
        "<div><div class='brand'>Danish AI</div></div>"
        "</div>"
        "<div class='tagline'>Your Intelligent AI Assistant</div>",
        unsafe_allow_html=True
    )

    pages = ["Dashboard", "AI Chat", "Usage & Stats", "Settings"]
    icons = {"Dashboard": "🏠", "AI Chat": "💬", "Usage & Stats": "📶", "Settings": "⚙️"}

    for p in pages:
        selected = st.session_state.page == p
        if st.button(f"{icons[p]}  {p}", key=f"nav_{p}", use_container_width=True,
                     type="primary" if selected else "secondary"):
            st.session_state.page = p
            st.rerun()

    st.markdown("<div class='nav-label'>CHAT</div>", unsafe_allow_html=True)

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div class='pro-card'>"
        "<div class='pro-title'>👑 Danish AI Premium</div>"
        "<div class='pro-text'>Unlock more power and exclusive features.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("Upgrade Now", use_container_width=True):
        st.toast("Premium isn't wired up yet — add your billing flow here.")

    st.markdown(
        "<div class='profile-row'>"
        f"<div class='profile-avatar'>{st.session_state.user_name[0].upper()}</div>"
        "<div>"
        f"<div class='profile-name'>{st.session_state.user_name}</div>"
        "<div class='profile-plan'>Free Plan</div>"
        "</div></div>",
        unsafe_allow_html=True
    )

# ============================================================
# GREETING HEADER (shown on Dashboard & AI Chat)
# ============================================================

def greeting_word():
    h = datetime.now().hour
    if h < 12:
        return "Good morning"
    if h < 17:
        return "Good afternoon"
    return "Good evening"


def render_header(subtitle):
    now = datetime.now()
    st.markdown(
        "<div class='greeting-row'>"
        "<div>"
        f"<div class='greeting-title'>{greeting_word()}, "
        f"<span class='greeting-accent'>{st.session_state.user_name}</span> 👋</div>"
        f"<div class='greeting-sub'>{subtitle}</div>"
        "</div>"
        "<div class='date-card'>📅 " + now.strftime("%B %-d, %Y") +
        f"<div class='time'>{now.strftime('%-I:%M %p')}</div></div>"
        "</div>",
        unsafe_allow_html=True
    )

# ============================================================
# STAT CARDS
# ============================================================

def render_stat_cards():
    col1, col2, col3, col4 = st.columns(4)
    cards = [
        (col1, "💬", "#3b2069", "#c4b5fd", str(st.session_state.total_messages),
         "Messages", "Total messages", SPARK_PURPLE, "#a78bfa"),
        (col2, "🙋", "#173a63", "#93c5fd", str(st.session_state.questions_asked),
         "Questions", "Asked by you", SPARK_BLUE, "#60a5fa"),
        (col3, "🤖", "#154a3a", "#6ee7b7", str(st.session_state.ai_responses),
         "AI Responses", "From Danish AI", SPARK_GREEN, "#34d399"),
        (col4, "🔥", "#5a3512", "#fdba74", str(st.session_state.roast_count),
         "Roast Mode", "Funny roasts", SPARK_ORANGE, "#fb923c"),
    ]
    for col, icon, bg, fg, number, label, sub, spark, spark_color in cards:
        with col:
            st.markdown(
                "<div class='stat-card'>"
                f"<div class='stat-icon' style='background:{bg};color:{fg};'>{icon}</div>"
                f"<div class='stat-number'>{number}</div>"
                f"<div class='stat-label'>{label}</div>"
                f"<div class='stat-sub'>{sub}</div>"
                f"{sparkline(spark_color, spark)}"
                "</div>",
                unsafe_allow_html=True
            )

# ============================================================
# CHAT RENDERING HELPERS
# ============================================================

def render_messages(messages):
    for m in messages:
        role = m["role"]
        ts = m.get("time", "")
        if role == "user":
            st.markdown(
                "<div class='msg-row user'>"
                "<div class='avatar user'>🙂</div>"
                "<div>"
                f"<div class='bubble user'>{m['content']}</div>"
                f"<div class='msg-time'>{ts} ✓</div>"
                "</div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='msg-row'>"
                "<div class='avatar bot'>🤖</div>"
                "<div>"
                f"<div class='bubble bot'>{m['content']}</div>"
                f"<div class='msg-time'>{ts}</div>"
                "</div></div>",
                unsafe_allow_html=True
            )


def get_ai_reply(history, system_prompt):
    if client is None:
        return "⚠️ OpenAI is not connected. Please check your OPENAI_API_KEY in Streamlit Secrets."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}] +
                     [{"role": h["role"], "content": h["content"]} for h in history]
        )
        return response.choices[0].message.content
    except Exception as error:
        return "⚠️ Something went wrong while contacting the AI.\n\n" + str(error)

# ============================================================
# DASHBOARD PAGE
# ============================================================

if st.session_state.page == "Dashboard":

    render_header("Here's what's happening with Danish AI today.")
    render_stat_cards()

    st.markdown(
        "<div class='chat-panel'>"
        "<div class='chat-panel-head'>"
        "<div class='chat-panel-title'>"
        "<div class='chat-icon-badge'>💬</div>"
        "<div><div class='chat-title-text'>AI Chat</div>"
        "<div class='chat-sub-text'>Talk with Danish AI.</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    if st.session_state.messages:
        render_messages(st.session_state.messages[-6:])
    else:
        st.markdown(
            "<div class='welcome-card'>"
            "<div class='welcome-title'>How can I help you today?</div>"
            "<div class='welcome-text'>Ask me anything from the AI Chat tab to get started.</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# AI CHAT PAGE
# ============================================================

elif st.session_state.page == "AI Chat":

    render_header("Talk with Danish AI.")

    st.markdown(
        "<div class='chat-panel'>"
        "<div class='chat-panel-head'>"
        "<div class='chat-panel-title'>"
        "<div class='chat-icon-badge'>💬</div>"
        "<div><div class='chat-title-text'>AI Chat</div>"
        "<div class='chat-sub-text'>Talk with Danish AI.</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    if not st.session_state.messages:
        st.markdown(
            "<div class='welcome-card'>"
            "<div class='welcome-title'>How can I help you today?</div>"
            "<div class='welcome-text'>Ask me anything. I can help with Python, AI, software "
            "engineering, business ideas, writing, learning and everyday questions.</div>"
            "</div>",
            unsafe_allow_html=True
        )

    render_messages(st.session_state.messages)

    roast_toggle = st.toggle("⚡ Roast Mode", value=st.session_state.roast_mode)
    st.session_state.roast_mode = roast_toggle

    user_input = st.chat_input("Type your message...")

    if user_input:
        now_str = datetime.now().strftime("%-I:%M %p")
        st.session_state.messages.append({"role": "user", "content": user_input, "time": now_str})
        st.session_state.total_messages += 1
        st.session_state.questions_asked += 1

        prompt = ROAST_PROMPT if st.session_state.roast_mode else NORMAL_PROMPT
        answer = get_ai_reply(st.session_state.messages, prompt)

        reply_time = datetime.now().strftime("%-I:%M %p")
        st.session_state.messages.append({"role": "assistant", "content": answer, "time": reply_time})
        st.session_state.total_messages += 1
        st.session_state.ai_responses += 1
        if st.session_state.roast_mode:
            st.session_state.roast_count += 1

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# USAGE & STATS PAGE
# ============================================================

elif st.session_state.page == "Usage & Stats":

    st.markdown("<div class='section-title'>📶 Usage & Stats</div>", unsafe_allow_html=True)
    render_stat_cards()

    st.markdown("")
    st.info(
        "💡 Stats are currently session-based. Later we can add user accounts, "
        "permanent usage statistics and analytics."
    )

# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown("<div class='section-title'>⚙️ Settings</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='welcome-card'>"
        "<div class='welcome-title'>Danish AI Settings</div>"
        "<div class='welcome-text'>Manage your AI experience.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.session_state.user_name = st.text_input("Display name", value=st.session_state.user_name)

    st.checkbox(
        "Enable Roast Mode by default",
        value=st.session_state.roast_mode,
        key="roast_setting"
    )
    st.session_state.roast_mode = st.session_state.roast_setting

    st.markdown("### AI Information")
    st.write("**Assistant:** Danish AI")
    st.write("**Model:** GPT-4o-mini")
    st.write("**API Status:** " + ("Connected ✅" if client is not None else "Not connected ⚠️"))

    st.markdown("### Conversation")
    if st.button("Clear all messages", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_messages = 0
        st.session_state.questions_asked = 0
        st.session_state.ai_responses = 0
        st.session_state.roast_count = 0
        st.success("Conversation cleared.")
        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<div class='footer-note'>Danish AI • Your Intelligent AI Assistant 💜</div>",
    unsafe_allow_html=True
)
