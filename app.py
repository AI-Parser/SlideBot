import streamlit as st
import tempfile
import os

from modules.slide_parser import parse_pptx
from modules.narrator import narrate_slide
from modules.vector_index import SlideVectorIndex
from modules.qa_engine import ask_question
from modules.summarizer import summarize_feedback

# --- App Config ---
st.title("📊 PPT Presentation Assistant")
st.markdown("Upload a `.pptx` file, ask questions, and get smart summaries with narration.")

# --- State ---
if "slides" not in st.session_state:
    st.session_state.slides = []
if "index" not in st.session_state:
    st.session_state.index = None
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- API Key ---
with st.sidebar:
    st.subheader("🔑 OpenAI API Key")
    api_key = st.text_input("Enter your key", type="password")
    print(api_key)
    if api_key:
        st.session_state.api_key = api_key

# --- Upload PPTX ---
ppt_file = st.file_uploader("Upload PPTX File", type=["pptx"])

if ppt_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
        tmp.write(ppt_file.read())
        tmp_path = tmp.name

    slides = parse_pptx(tmp_path, st.session_state.api_key)
    st.session_state.slides = slides

    st.success(f"Parsed {len(slides)} slides.")
    os.remove(tmp_path)

    # Vector Indexing
    index = SlideVectorIndex()
    index.add_slides(slides)
    st.session_state.index = index

    # Slide Narration
    st.subheader("🗣 Narrate Slides")
    for i, slide in enumerate(slides):
        with st.expander(f"Slide {i+1}: {slide['title']}"):
            st.write(slide["content"])
            if st.button(f"🔊 Narrate Slide {i+1}", key=f"narrate_{i}"):
                narrate_slide(slide["title"], slide["content"])

# --- Q&A Section ---
if st.session_state.slides:
    st.subheader("❓ Ask Questions")
    question = st.text_input("What would you like to ask about the slides?")
    print(question)

    if question and st.session_state.api_key:
        relevant_slides = st.session_state.index.query(question)
        answer = ask_question(question, relevant_slides, st.session_state.api_key)
        st.markdown("**Answer:**")
        st.write(answer)

# --- Feedback Collection ---
if st.session_state.slides:
    st.subheader("✍️ Viewer Feedback")
    feedback = st.text_area("Enter feedback here")
    if st.button("Submit Feedback"):
        if feedback.strip():
            st.session_state.feedback.append(feedback.strip())
            st.success("Feedback submitted.")
        else:
            st.warning("Please enter some feedback.")

# --- Summary ---
if st.session_state.feedback:
    st.subheader("📄 Summarize Feedback")
    if st.button("Generate Summary"):
        if st.session_state.api_key:
            summary = summarize_feedback(st.session_state.feedback, st.session_state.api_key)
            st.markdown("**Summary:**")
            st.write(summary)
        else:
            st.error("API key required to generate summary.")
