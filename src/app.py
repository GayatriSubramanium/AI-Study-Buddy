import streamlit as st
import openai
import os
import PyPDF2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API key from .env
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded correctly
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please check your .env file.")

# Set the OpenAI API key
openai.api_key = api_key

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("📚 AI-Powered Study Buddy")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# PDF Upload Section
uploaded_file = st.file_uploader("Upload Lecture Notes (PDF)", type="pdf")
user_input = ""

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() or "" for page in reader.pages])
    st.text_area("Extracted Text", text[:1000])
    user_input = text

# Manual Input Section
manual_text = st.text_area("Or paste your text/notes below:")
if manual_text:
    user_input = manual_text

# Summarize Notes
if st.button("Summarize Notes") and user_input:
    with st.spinner("Generating summary..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize this study material: {user_input}"}]
            )
            summary = response['choices'][0]['message']['content']
            st.markdown("### Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"❌ Failed to generate summary: {e}")

# Generate Quiz Questions
if st.button("Generate Quiz") and user_input:
    with st.spinner("Creating quiz questions..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Create 5 MCQs based on this material: {user_input}"}]
            )
            quiz = response['choices'][0]['message']['content']
            st.markdown("### Quiz Questions")
            st.write(quiz)
        except Exception as e:
            st.error(f"❌ Failed to generate quiz: {e}")

# Contextual Q&A Section
st.markdown("---")
st.subheader("Ask a Question")
question = st.text_input("Your Question")

if st.button("Get Answer") and question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("Answering..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history
            )
            answer = response['choices'][0]['message']['content']
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.markdown("### Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Failed to get answer: {e}")

# Display chat history
st.markdown("---")
with st.expander("View Conversation History"):
    for msg in st.session_state.chat_history:
        role = "🧑‍🎓 You" if msg["role"] == "user" else "🤖 Study Buddy"
        st.markdown(f"**{role}:** {msg['content']}")
