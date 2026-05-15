import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# ================= LOAD ENV =================
load_dotenv()

# ================= MODEL =================
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Mood Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

/* Chat Box */
.chat-container {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

/* User Chat */
.user-msg {
    background: #2563eb;
    padding: 12px;
    border-radius: 12px;
    color: white;
    margin-bottom: 10px;
}

/* AI Chat */
.ai-msg {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 12px;
    border-radius: 12px;
    color: #f1f5f9;
    margin-bottom: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    padding: 10px;
    font-weight: 600;
}

/* Radio */
div[role="radiogroup"] {
    gap: 20px;
}

/* Input */
.stChatInput input {
    background-color: #1e293b !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<p class="main-title">🤖 AI Mood Chatbot</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Advanced AI chatbot with multiple personalities powered by Mistral AI</p>',
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
with st.sidebar:

    st.title("⚙️ Control Panel")

    st.markdown("---")

    mode_choice = st.radio(
        "Choose AI Personality",
        ["😡 Angry", "😂 Funny", "😢 Sad"]
    )

    st.markdown("---")

    temperature = st.slider(
        "AI Creativity",
        0.0,
        1.0,
        0.9
    )

    st.markdown("---")

    st.info("""
    Features:
    - Multi AI personalities
    - Session memory
    - Real-time responses
    - Modern UI
    """)

# ================= MODES =================
if mode_choice == "😡 Angry":
    mode = "You are an angry AI assistant. Respond aggressively."
    avatar = "😡"

elif mode_choice == "😂 Funny":
    mode = "You are a funny AI assistant. Use humor and jokes."
    avatar = "😂"

else:
    mode = "You are a sad AI assistant. Respond emotionally."
    avatar = "😢"

# ================= SESSION STATE =================
if (
    "messages" not in st.session_state
    or st.session_state.get("current_mode") != mode
):

    st.session_state.current_mode = mode
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# ================= DISPLAY CHAT =================
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        st.markdown(
            f"""
            <div class="user-msg">
            👤 {msg.content}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif isinstance(msg, AIMessage):

        st.markdown(
            f"""
            <div class="ai-msg">
            {avatar} {msg.content}
            </div>
            """,
            unsafe_allow_html=True
        )

# ================= CHAT INPUT =================
user_input = st.chat_input("Type your message...")

if user_input:

    if user_input == "0":
        st.warning("Conversation ended.")
        st.stop()

    # Add User Message
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    # Refresh user message
    st.rerun()

# ================= GENERATE RESPONSE =================
if (
    len(st.session_state.messages) > 0
    and isinstance(st.session_state.messages[-1], HumanMessage)
):

    with st.spinner("AI is typing..."):

        response = model.invoke(
            st.session_state.messages
        )

        st.session_state.messages.append(
            AIMessage(content=response.content)
        )

        st.rerun()

# ================= FOOTER =================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = [
            SystemMessage(content=mode)
        ]
        st.rerun()

with col2:
    st.download_button(
        "📥 Download Chat",
        str(st.session_state.messages),
        file_name="chat_history.txt"
    )

with col3:
    st.button("🌙 Dark Mode Enabled")

st.markdown(
    "<center><small>Built with Streamlit + LangChain + Mistral AI</small></center>",
    unsafe_allow_html=True
)