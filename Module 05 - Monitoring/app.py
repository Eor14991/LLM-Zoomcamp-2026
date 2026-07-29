import streamlit as st
from assistant import create_assistant

st.title("Course Assistant")

@st.cache_resource
def load_assistant():
    return create_assistant()

with st.spinner("Loading AI Assistant for the first time..."):
    assistant = load_assistant()

user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_input.strip():
        with st.spinner("Processing..."):
            answer = assistant.rag_pipeline(user_input)
            st.success("Completed!")
            st.write(answer)

            record = assistant.last_call
            st.write(f"Response time: {record.response_time:.2f}s")
            st.write(f"Prompt tokens: {record.prompt_tokens}")
            st.write(f"Completion tokens: {record.completion_tokens}")
            st.write(f"Cost: ${record.cost:.4f}")
    else:
        st.warning("Please enter a question first.")