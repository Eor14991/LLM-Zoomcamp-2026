import streamlit as st
from assistant import create_assistant
from db_save import save_conversation
from db_feedback import save_feedback
from judge import evaluate_relevance
from db_feedback import save_feedback
st.title("Course Assistant")

@st.cache_resource
def load_assistant():
    return create_assistant()

with st.spinner("Loading AI Assistant for the first time..."):
    assistant = load_assistant()

user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    with st.spinner("Processing..."):
        answer = assistant.rag_pipeline(user_input)
        st.success("Completed!")
        st.write(answer)

        record = assistant.last_call
        st.write(f"Response time: {record.response_time:.2f}s")
        st.write(f"Input_tokens: {record.input_tokens}")
        st.write(f"Output_tokens: {record.output_tokens}")
        st.write(f"Cost: ${record.cost:.4f}")

        conversation_id = save_conversation(record, user_input, "llm-zoomcamp")
        st.session_state.conversation_id = conversation_id

        relevance, explanation = evaluate_relevance(user_input, answer)
        save_feedback(conversation_id, "judge",
                      relevance=relevance, explanation=explanation)
        st.write(f"Relevance: {relevance}")
        st.write(f"Explanation: {explanation}")

col1, col2 = st.columns(2)
with col1:
    if st.button("+1"):
        cid = st.session_state.conversation_id
        save_feedback(cid, "user", score=1)
        st.write("Thanks!")

with col2:
    if st.button("-1"):
        cid = st.session_state.conversation_id
        save_feedback(cid, "user", score=-1)
        st.write("Thanks for the feedback!")
    else:
        st.warning("Please enter a question first.")

