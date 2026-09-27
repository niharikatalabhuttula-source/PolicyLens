import streamlit as st
import os
from ingestion.pdf_loader import extract_text_by_page
from ingestion.text_cleaner import clean_text
from ingestion.chunker import chunk_pages
from retrieval.vector_store import add_chunks, reset_collection
from core.qa_pipeline import answer_question
from core.summarizer import summarize_document
from core.document_info import extract_scheme_info

st.set_page_config(page_title="PolicyLens", page_icon=None, layout="wide")

# ---------------------------------------------------------------------------
# Global styling — forces a consistent light, formal theme regardless of the
# visitor's system/browser theme, and covers every Streamlit component used
# in this app (buttons, file uploader, chat input, header, tabs).
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ---- Base app surface ---- */
    .stApp {
        background-color: #ffffff;
    }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: #1a1f2b;
    }
    header[data-testid="stHeader"] {
        background-color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: #f7f8fa;
        border-right: 1px solid #e1e4e8;
    }
        div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 1px solid #d5dae0 !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #1a1f2b !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8a8f98 !important;
    }

    /* ---- Titles ---- */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1f2b;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }
    .subtitle {
        color: #5a6270;
        font-size: 1rem;
        margin-top: 0.2rem;
        margin-bottom: 1.6rem;
    }
    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #6b7280;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    /* ---- Content cards (summary, structured info, source badges) ---- */
    .answer-card {
        background-color: #f7f8fa;
        border: 1px solid #e1e4e8;
        border-left: 3px solid #2c3e50;
        border-radius: 6px;
        padding: 1.1rem 1.3rem;
        margin: 0.5rem 0 1rem 0;
        line-height: 1.55;
    }
    .answer-card, .answer-card * {
        color: #1a1f2b !important;
    }
    .info-field-label {
        color: #2c3e50 !important;
        font-weight: 700;
        font-size: 0.92rem;
        margin-top: 0.9rem;
        border-bottom: 1px solid #e1e4e8;
        padding-bottom: 0.2rem;
    }
    .source-badge {
        display: inline-block;
        background-color: #eef1f4;
        color: #2c3e50 !important;
        border: 1px solid #d5dae0;
        border-radius: 4px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin-right: 6px;
        font-weight: 500;
    }
    .disclaimer-box {
        font-size: 0.82rem;
        color: #6b7280;
    }

    /* ---- Tabs ---- */
    button[data-baseweb="tab"] {
        color: #5a6270 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2c3e50 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #2c3e50 !important;
    }

    /* ---- Buttons (secondary / default) ---- */
    .stButton > button {
        background-color: #ffffff !important;
        border: 1px solid #d5dae0 !important;
        border-radius: 6px !important;
    }
    .stButton > button, .stButton > button p, .stButton > button span {
        color: #1a1f2b !important;
    }
    .stButton > button:hover {
        border-color: #2c3e50 !important;
    }
    .stButton > button:hover p, .stButton > button:hover span {
        color: #2c3e50 !important;
    }

    /* ---- Primary buttons (Generate Summary, Extract Info) ---- */
    .stButton > button[kind="primary"] {
        background-color: #2c3e50 !important;
        border: none !important;
    }
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        color: #ffffff !important;
    }

    /* ---- File uploader ---- */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #f7f8fa !important;
        border: 1px dashed #c5cad2 !important;
    }
    section[data-testid="stFileUploaderDropzone"] * {
        color: #1a1f2b !important;
    }
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #ffffff !important;
        border: 1px solid #d5dae0 !important;
    }
    section[data-testid="stFileUploaderDropzone"] button * {
        color: #1a1f2b !important;
    }
    div[data-testid="stFileUploaderFile"] {
        background-color: #ffffff !important;
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stFileUploaderFile"] * {
        color: #1a1f2b !important;
    }

    /* ---- Chat messages and input ---- */
    div[data-testid="stChatMessage"] {
        background-color: #f7f8fa !important;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
    }
    div[data-testid="stChatMessage"] * {
        color: #1a1f2b !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 1px solid #d5dae0 !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #1a1f2b !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8a8f98 !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #2c3e50 !important;
    }

    /* ---- Metrics (Pages, Sections indexed) ---- */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
    }
    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #1a1f2b !important;
    }

    /* ---- Alerts (info / success / warning / error) ---- */
    div[data-testid="stAlert"] * {
        color: #1a1f2b !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
if "processed_filename" not in st.session_state:
    st.session_state.processed_filename = None
if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {"pages": 0, "chunks": 0}

FIELD_LABELS = {
    "scheme_name": "Scheme Name",
    "eligibility": "Eligibility",
    "benefits": "Benefits",
    "required_documents": "Required Documents",
    "application_process": "Application Process",
    "important_conditions": "Important Conditions",
}


def clear_document_state():
    st.session_state.processed_filename = None
    st.session_state.full_text = ""
    st.session_state.chat_history = []
    st.session_state.doc_stats = {"pages": 0, "chunks": 0}
    st.session_state.pop("summary", None)
    st.session_state.pop("scheme_info", None)


# ---------------------------------------------------------------------------
# Sidebar — upload and document status
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### PolicyLens")
    st.caption("Government Scheme & Policy Document Assistant")
    st.divider()

    st.markdown('<p class="section-label">Upload Document</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Government scheme or policy PDF",
        type="pdf",
        label_visibility="collapsed"
    )

    if uploaded_file is not None and st.session_state.processed_filename != uploaded_file.name:
        save_path = os.path.join("data", "uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Processing document. This may take a minute."):
            reset_collection()  # clear any previously indexed document

            pages = extract_text_by_page(save_path)
            for page in pages:
                page["text"] = clean_text(page["text"])

            chunks = chunk_pages(pages)
            failed = add_chunks(chunks)

            clear_document_state()
            st.session_state.full_text = "\n\n".join(page["text"] for page in pages)
            st.session_state.processed_filename = uploaded_file.name
            st.session_state.doc_stats = {"pages": len(pages), "chunks": len(chunks)}

        if failed:
            st.warning(f"{len(failed)} section(s) could not be indexed due to a temporary service issue.")
        st.success("Document ready.")

    if st.session_state.processed_filename:
        st.divider()
        st.markdown('<p class="section-label">Active Document</p>', unsafe_allow_html=True)
        st.write(st.session_state.processed_filename)

        col1, col2 = st.columns(2)
        col1.metric("Pages", st.session_state.doc_stats["pages"])
        col2.metric("Sections indexed", st.session_state.doc_stats["chunks"])

        if st.button("Clear document", use_container_width=True):
            clear_document_state()
            st.rerun()

    st.divider()
    st.markdown(
        '<p class="disclaimer-box">This tool provides information support only. '
        'It is not a legal authority and does not replace official verification '
        'with the relevant government department.</p>',
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.markdown('<p class="main-title">PolicyLens</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A document-grounded assistant for understanding '
    'government scheme and policy information.</p>',
    unsafe_allow_html=True
)

if not st.session_state.processed_filename:
    st.info("Upload a government scheme or policy PDF from the panel on the left to begin.")
else:
    tab_chat, tab_summary, tab_info = st.tabs(["Ask Questions", "Summary", "Structured Information"])

    # --- Ask Questions ---
    with tab_chat:
        st.markdown('<p class="section-label">Suggested Questions</p>', unsafe_allow_html=True)
        sample_cols = st.columns(3)
        sample_questions = [
            "Who is eligible?",
            "What are the benefits?",
            "What documents are required?",
        ]
        clicked_sample = None
        for col, sq in zip(sample_cols, sample_questions):
            if col.button(sq, use_container_width=True):
                clicked_sample = sq

        st.divider()

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and msg.get("pages"):
                    badges = "".join(
                        f'<span class="source-badge">Page {p}</span>' for p in msg["pages"]
                    )
                    st.markdown(badges, unsafe_allow_html=True)
                if msg["role"] == "assistant" and msg.get("warning"):
                    st.warning(msg["warning"])

        user_question = st.chat_input("Ask about eligibility, benefits, documents, or deadlines")
        question_to_ask = clicked_sample or user_question

        if question_to_ask:
            st.session_state.chat_history.append({"role": "user", "content": question_to_ask})
            with st.chat_message("user"):
                st.markdown(question_to_ask)

            with st.chat_message("assistant"):
                with st.spinner("Searching the document..."):
                    result = answer_question(question_to_ask)

                st.markdown(result["answer"])

                warning_text = None
                if result["pages"]:
                    badges = "".join(
                        f'<span class="source-badge">Page {p}</span>' for p in result["pages"]
                    )
                    st.markdown(badges, unsafe_allow_html=True)

                if not result["numeric_grounding"]["all_numbers_grounded"]:
                    warning_text = (
                        "Some figures in this answer could not be fully verified against "
                        "the source text. Please confirm against the original document."
                    )
                    st.warning(warning_text)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result["answer"],
                "pages": result["pages"],
                "warning": warning_text,
            })

    # --- Summary ---
    with tab_summary:
        st.markdown('<p class="section-label">Document Summary</p>', unsafe_allow_html=True)
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Summarizing. This can take 15-20 seconds for a full document."):
                st.session_state.summary = summarize_document(st.session_state.full_text)

        if "summary" in st.session_state:
            st.markdown(f'<div class="answer-card">{st.session_state.summary}</div>', unsafe_allow_html=True)

    # --- Structured Information ---
    with tab_info:
        st.markdown('<p class="section-label">Key Scheme Details</p>', unsafe_allow_html=True)
        if st.button("Extract Scheme Information", type="primary"):
            with st.spinner("Extracting structured information. This can take 15-20 seconds."):
                st.session_state.scheme_info = extract_scheme_info(st.session_state.full_text)

        if "scheme_info" in st.session_state:
            info = st.session_state.scheme_info
            if "error" in info:
                st.error(info["error"])
            else:
                for key, value in info.items():
                    label = FIELD_LABELS.get(key, key.replace("_", " ").title())
                    st.markdown(f'<p class="info-field-label">{label}</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="answer-card">{value}</div>', unsafe_allow_html=True)