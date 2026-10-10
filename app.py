import streamlit as st

from Modules.pdf_reader import extract_text
from Modules.chunking import create_chunks
from Modules.embeddings import create_embeddings, embedding_model
from Modules.vector_score import create_index, search_similar
from Modules.llm import generate_answer


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# THEME COLORS
# =========================================================

if st.session_state.dark_mode:

    background = "#0B1120"
    sidebar = "#111827"
    card = "#151F32"
    text = "#F8FAFC"
    muted = "#94A3B8"
    border = "#263449"
    accent = "#6366F1"

else:

    background = "#F8FAFC"
    sidebar = "#FFFFFF"
    card = "#FFFFFF"
    text = "#111827"
    muted = "#64748B"
    border = "#E2E8F0"
    accent = "#4F46E5"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       HIDE STREAMLIT TOP BAR
       ===================================================== */

    [data-testid="stHeader"] {{
        display: none;
    }}

    [data-testid="stToolbar"] {{
        display: none;
    }}

    [data-testid="stAppDeployButton"] {{
        display: none;
    }}


    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {{
        background-color: {background};
        color: {text};
    }}

    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {{
        background-color: {sidebar};
        border-right: 1px solid {border};
    }}

    [data-testid="stSidebar"] * {{
        color: {text};
    }}


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {{
        width: 100%;
        border-radius: 12px;
        border: 1px solid {border};
        background-color: {card};
        color: {text};
        font-weight: 600;
        min-height: 45px;
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        border-color: {accent};
        color: {accent};
        transform: translateY(-1px);
    }}


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    [data-testid="stChatInput"] {{
        border-radius: 14px;
    }}


    /* =====================================================
       CHAT MESSAGE TEXT
       ===================================================== */

    [data-testid="stChatMessage"] p {{
        color: {text} !important;
    }}

    [data-testid="stChatMessage"] li {{
        color: {text} !important;
    }}

    [data-testid="stChatMessage"] span {{
        color: {text} !important;
    }}

    [data-testid="stChatMessage"] div {{
        color: {text};
    }}


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {{
        border-color: {border};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("### 🎓 College AI Assistant")

    st.caption(
        "Your intelligent college information assistant."
    )

    st.divider()


    # =====================================================
    # NEW CHAT
    # =====================================================

    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # =====================================================
    # APPEARANCE
    # =====================================================

    st.markdown("### ⚙️ Appearance")

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode
    )

    if dark_mode != st.session_state.dark_mode:

        st.session_state.dark_mode = dark_mode

        st.rerun()


    st.divider()


    # =====================================================
    # FEATURES
    # =====================================================

    st.markdown("### ✨ Features")

    st.markdown(
        """
        📚 College information

        💬 Natural language questions

        🤖 AI-powered answers

        🔎 Relevant document search

        ⚡ Fast information access
        """
    )

    st.divider()

    st.caption(
        "FutureTech Institute of Technology"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    f"""
    <h1 style="
        text-align:center;
        font-size:38px;
        margin-top:0;
        margin-bottom:4px;
        color:{text};
    ">
        🎓 FutureTech Institute of Technology
    </h1>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <p style="
        text-align:center;
        font-size:18px;
        font-weight:700;
        color:{accent};
        margin-top:0;
        margin-bottom:4px;
    ">
        College AI Assistant
    </p>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <p style="
        text-align:center;
        font-size:14px;
        color:{muted};
        margin-top:0;
        margin-bottom:20px;
    ">
        Ask questions. Find information. Get answers instantly.
    </p>
    """,
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# LOAD COLLEGE DATA
# =========================================================

@st.cache_resource
def load_college_data():

    pdf_path = "Data/college.pdf"

    with open(pdf_path, "rb") as pdf_file:

        text = extract_text(pdf_file)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = create_index(embeddings)

    return chunks, index


chunks, index = load_college_data()


# =========================================================
# DOCUMENT STATUS
# =========================================================

# st.success("🟢 College Document Ready")

# st.caption(
#     "The AI assistant is ready to answer questions "
#     "from the college information document."
# )


# =========================================================
# WELCOME MESSAGE
# =========================================================

# if len(st.session_state.messages) == 0:

#     st.subheader("👋 Welcome to College AI Assistant")

#     st.write(
#         "Ask questions about courses, admissions, eligibility, "
#         "facilities, departments, placements and other college "
#         "information. The assistant will provide answers based "
#         "on the available college document."
#     )


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

selected_question = None


if len(st.session_state.messages) == 0:

    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "📚 What courses are offered by the college?",
            use_container_width=True
        ):

            selected_question = (
                "What courses are offered by the college?"
            )


        if st.button(
            "🎯 What are the eligibility criteria?",
            use_container_width=True
        ):

            selected_question = (
                "What are the eligibility criteria?"
            )


    with col2:

        if st.button(
            "📝 What is the admission process?",
            use_container_width=True
        ):

            selected_question = (
                "What is the admission process?"
            )


        if st.button(
            "🏫 What facilities does the college provide?",
            use_container_width=True
        ):

            selected_question = (
                "What facilities does the college provide?"
            )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

typed_question = st.chat_input(
    "Ask something about the college..."
)


question = (
    selected_question
    if selected_question
    else typed_question
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # -----------------------------------------------------
    # CREATE QUERY EMBEDDING
    # -----------------------------------------------------

    query_vector = embedding_model.embed_query(
        question
    )


    # -----------------------------------------------------
    # SEARCH RELEVANT CHUNKS
    # -----------------------------------------------------

    results = search_similar(
        query_vector,
        index,
        chunks
    )


    # -----------------------------------------------------
    # CREATE CONTEXT
    # -----------------------------------------------------

    context = "\n\n".join(results)


    # -----------------------------------------------------
    # GENERATE AI ANSWER
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking... 🤔"):

            answer = generate_answer(
                question,
                context
            )

        st.write(answer)


    # -----------------------------------------------------
    # SAVE ASSISTANT ANSWER
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎓 FutureTech Institute of Technology • "
    "College AI Assistant • Powered by AI"
)