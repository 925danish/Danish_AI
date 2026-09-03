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

defaults = {
    "messages": [],
    "page": "AI Chat",
    "total_messages": 0,
    "questions_asked": 0,
    "ai_responses": 0,
    "roast_count": 0,
    "roast_mode": False,
    "user_name": "Danish",
    "theme": "dark",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
# THEME PALETTES
# ============================================================

DARK = {
    "bg": "#0f1115", "sidebar_bg": "#14161c", "border": "#2a2d35",
    "text": "#f3f4f6", "text_soft": "#9199a8", "text_muted": "#6b7280",
    "card_bg": "#181a20", "input_bg": "#1a1c22",
    "accent": "#6366f1", "accent_hover": "#7477f3", "accent_soft_bg": "#1e1b3a", "accent_soft_fg": "#a5b4fc",
    "green_bg": "#122420", "green_fg": "#6ee7b7",
    "amber_bg": "#2a2010", "amber_fg": "#fbbf24",
    "bot_bubble": "#20222a", "avatar_bg": "#2a2d35",
}

LIGHT = {
    "bg": "#f4f5f7", "sidebar_bg": "#ffffff", "border": "#e5e7eb",
    "text": "#111827", "text_soft": "#4b5563", "text_muted": "#6b7280",
    "card_bg": "#ffffff", "input_bg": "#ffffff",
    "accent": "#4338ca", "accent_hover": "#3730a3", "accent_soft_bg": "#eef2ff", "accent_soft_fg": "#4338ca",
    "green_bg": "#ecfdf5", "green_fg": "#059669",
    "amber_bg": "#fffbeb", "amber_fg": "#b45309",
    "bot_bubble": "#f3f4f6", "avatar_bg": "#e5e7eb",
}

T = DARK if st.session_state.theme == "dark" else LIGHT

# ============================================================
# STYLE
# ============================================================

css = f"""
<style>
.stApp{{background:{T['bg']};color:{T['text']};}}
[data-testid="stSidebar"]{{background:{T['sidebar_bg']};border-right:1px solid {T['border']};}}
[data-testid="stSidebar"] *{{color:{T['text']};}}
#MainMenu, footer, header{{visibility:hidden;}}

.brand-row{{display:flex;align-items:center;gap:10px;margin-top:4px;margin-bottom:2px;}}
.brand-logo{{
    width:38px;height:38px;border-radius:10px;background:{T['accent']};
    display:flex;align-items:center;justify-content:center;font-size:18px;
}}
.brand{{font-size:20px;font-weight:600;letter-spacing:-0.3px;line-height:1.1;color:{T['text']};}}
.tagline{{color:{T['text_muted']};font-size:12px;margin-top:0;margin-bottom:20px;}}
.nav-label{{color:{T['text_muted']};font-size:11px;letter-spacing:0.5px;margin:16px 0 6px 4px;}}

.pro-card{{
    background:{T['accent_soft_bg']};border:1px solid {T['border']};
    border-radius:14px;padding:16px;margin-top:16px;
}}
.pro-title{{font-size:14px;font-weight:600;display:flex;align-items:center;gap:6px;color:{T['accent_soft_fg']};}}
.pro-text{{font-size:12px;margin-top:5px;color:{T['text_soft']};line-height:1.4;}}

.profile-row{{
    display:flex;align-items:center;gap:10px;
    border-top:1px solid {T['border']};padding-top:14px;margin-top:14px;
}}
.profile-avatar{{
    width:34px;height:34px;border-radius:50%;background:{T['accent']};
    display:flex;align-items:center;justify-content:center;font-weight:600;color:#fff;
}}
.profile-name{{font-size:13.5px;font-weight:600;color:{T['text']};}}
.profile-plan{{font-size:11px;color:{T['text_muted']};}}

.greeting-row{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;flex-wrap:wrap;gap:12px;}}
.greeting-title{{font-size:26px;font-weight:600;margin:0;color:{T['text']};}}
.greeting-accent{{color:{T['accent']};}}
.greeting-sub{{color:{T['text_soft']};font-size:13.5px;margin-top:4px;}}
.date-card{{
    background:{T['card_bg']};border:1px solid {T['border']};border-radius:12px;
    padding:10px 16px;font-size:12.5px;color:{T['text_soft']};min-width:140px;text-align:right;
}}
.date-card .time{{font-size:15px;font-weight:600;color:{T['text']};}}

.stat-card{{
    background:{T['card_bg']};border:1px solid {T['border']};border-radius:14px;
    padding:18px;min-height:120px;
}}
.stat-icon{{
    width:36px;height:36px;border-radius:9px;
    display:flex;align-items:center;justify-content:center;font-size:17px;margin-bottom:12px;
}}
.stat-number{{font-size:24px;font-weight:600;margin:2px 0;color:{T['text']};}}
.stat-label{{font-size:13px;font-weight:600;color:{T['text']};}}
.stat-sub{{font-size:11.5px;color:{T['text_muted']};margin-top:1px;}}

.chat-panel{{
    background:{T['card_bg']};border:1px solid {T['border']};border-radius:16px;
    padding:20px;margin-top:22px;
}}
.chat-panel-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:10px;}}
.chat-panel-title{{display:flex;align-items:center;gap:11px;}}
.chat-icon-badge{{
    width:34px;height:34px;border-radius:9px;background:{T['accent_soft_bg']};
    display:flex;align-items:center;justify-content:center;font-size:16px;
}}
.chat-title-text{{font-size:17px;font-weight:600;color:{T['text']};}}
.chat-sub-text{{font-size:12px;color:{T['text_muted']};margin-top:1px;}}

.msg-row{{display:flex;gap:10px;margin-bottom:14px;align-items:flex-end;}}
.msg-row.user{{flex-direction:row-reverse;}}
.avatar{{
    width:30px;height:30px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;font-size:14px;background:{T['avatar_bg']};
}}
.avatar.user{{background:{T['accent_soft_bg']};}}
.bubble{{max-width:65%;padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.5;}}
.bubble.user{{background:{T['accent']};color:#fff;border-bottom-right-radius:4px;}}
.bubble.bot{{background:{T['bot_bubble']};color:{T['text']};border-bottom-left-radius:4px;}}
.msg-time{{font-size:10.5px;color:{T['text_muted']};margin-top:4px;}}
.msg-row.user .msg-time{{text-align:right;}}

.welcome-card{{background:{T['accent_soft_bg']};border:1px solid {T['border']};border-radius:14px;padding:18px;margin-bottom:14px;}}
.welcome-title{{font-size:16px;font-weight:600;color:{T['text']};}}
.welcome-text{{color:{T['text_soft']};margin-top:6px;line-height:1.5;font-size:13px;}}

.section-title{{font-size:22px;font-weight:600;margin-bottom:14px;color:{T['text']};}}
.footer-note{{text-align:center;color:{T['text_muted']};font-size:11.5px;padding:24px 0 4px 0;}}

.stButton>button{{
    border-radius:10px;border:1px solid {T['border']};background:{T['input_bg']};
    color:{T['text']};font-weight:500;
}}
.stButton>button:hover{{border-color:{T['accent']};color:{T['accent']};}}
button[kind="primary"]{{
    background:{T['accent']}!important;border:none!important;color:#fff!important;
}}
button[kind="primary"]:hover{{background:{T['accent_hover']}!important;}}
div[data-testid="stChatInput"]{{border-top:1px solid {T['border']};padding-top:12px;}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


def sparkline(color, points):
    w, h = 220, 34
    step = w / (len(points) - 1)
    coords = " ".join(f"{i*step:.1f},{h - p*h:.1f}" for i, p in enumerate(points))
    return (
        f'<svg width="100%" height="34" viewBox="0 0 {w} {h}" '
        f'preserveAspectRatio="none" style="margin-top:8px;">'
        f'<polyline points="{coords}" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


SPARK_A = [0.3, 0.55, 0.35, 0.7, 0.5, 0.8, 0.6]
SPARK_B = [0.4, 0.3, 0.6, 0.4, 0.65, 0.45, 0.55]
SPARK_C = [0.5, 0.65, 0.4, 0.6, 0.75, 0.55, 0.7]
SPARK_D = [0.35, 0.6, 0.3, 0.55, 0.4, 0.65, 0.5]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        "<div class='brand-row'>"
        "<div class='brand-logo'>🤖</div>"
        "<div><div class='brand'>Danish AI</div></div>"
        "</div>"
        "<div class='tagline'>Your intelligent AI assistant</div>",
        unsafe_allow_html=True
    )

    pages = ["AI Chat", "Dashboard", "Usage & Stats", "Settings"]
    icons = {"AI Chat": "💬", "Dashboard": "🏠", "Usage & Stats": "📶", "Settings": "⚙️"}

    for p in pages:
        selected = st.session_state.page == p
        if st.button(f"{icons[p]}  {p}", key=f"nav_{p}", use_container_width=True,
                     type="primary" if selected else "secondary"):
            st.session_state.page = p
            st.rerun()

    st.markdown("<div class='nav-label'>CHAT</div>", unsafe_allow_html=True)

    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div class='pro-card'>"
        "<div class='pro-title'>👑 Danish AI Premium</div>"
        "<div class='pro-text'>Unlock more power and exclusive features.</div>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("Upgrade now", use_container_width=True):
        st.toast("Premium isn't wired up yet — add your billing flow here.")

    st.markdown("<div class='nav-label'>APPEARANCE</div>", unsafe_allow_html=True)
    theme_choice = st.radio(
        "Theme", ["Dark", "Light"],
        index=0 if st.session_state.theme == "dark" else 1,
        horizontal=True, label_visibility="collapsed"
    )
    new_theme = theme_choice.lower()
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown(
        "<div class='profile-row'>"
        f"<div class='profile-avatar'>{st.session_state.user_name[0].upper()}</div>"
        "<div>"
        f"<div class='profile-name'>{st.session_state.user_name}</div>"
        "<div class='profile-plan'>Free plan</div>"
        "</div></div>",
        unsafe_allow_html=True
    )

# ============================================================
# HEADER
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
        (col1, "💬", T["accent_soft_bg"], T["accent_soft_fg"], str(st.session_state.total_messages),
         "Messages", "Total messages", SPARK_A, T["accent"]),
        (col2, "🙋", T["accent_soft_bg"], T["accent_soft_fg"], str(st.session_state.questions_asked),
         "Questions", "Asked by you", SPARK_B, T["accent"]),
        (col3, "🤖", T["green_bg"], T["green_fg"], str(st.session_state.ai_responses),
         "AI responses", "From Danish AI", SPARK_C, T["green_fg"]),
        (col4, "🔥", T["amber_bg"], T["amber_fg"], str(st.session_state.roast_count),
         "Roast mode", "Funny roasts", SPARK_D, T["amber_fg"]),
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
# CHAT HELPERS
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
                "<div class='avatar'>🤖</div>"
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
# AI CHAT PAGE (default landing page)
# ============================================================

if st.session_state.page == "AI Chat":

    render_header("Talk with Danish AI.")

    st.markdown(
        "<div class='chat-panel'>"
        "<div class='chat-panel-head'>"
        "<div class='chat-panel-title'>"
        "<div class='chat-icon-badge'>💬</div>"
        "<div><div class='chat-title-text'>AI chat</div>"
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

    roast_toggle = st.toggle("⚡ Roast mode", value=st.session_state.roast_mode)
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
# DASHBOARD PAGE
# ============================================================

elif st.session_state.page == "Dashboard":

    render_header("Here's what's happening with Danish AI today.")
    render_stat_cards()

    st.markdown(
        "<div class='chat-panel'>"
        "<div class='chat-panel-head'>"
        "<div class='chat-panel-title'>"
        "<div class='chat-icon-badge'>💬</div>"
        "<div><div class='chat-title-text'>AI chat</div>"
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
# USAGE & STATS PAGE
# ============================================================

elif st.session_state.page == "Usage & Stats":

    st.markdown("<div class='section-title'>📶 Usage & stats</div>", unsafe_allow_html=True)
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
        "<div class='welcome-title'>Danish AI settings</div>"
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

    st.markdown("### AI information")
    st.write("**Assistant:** Danish AI")
    st.write("**Model:** GPT-4o-mini")
    st.write("**API status:** " + ("Connected ✅" if client is not None else "Not connected ⚠️"))

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
    "<div class='footer-note'>Danish AI • Your intelligent AI assistant</div>",
    unsafe_allow_html=True
)
