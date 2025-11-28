import streamlit as st
from gemini_client import get_gemini_response

st.set_page_config(page_title="Gemini Chat", page_icon="💬", layout="centered")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.title("Chat with Gemini (Streamlit)")

# Show previous messages (skip system message)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Gemini:** {msg['content']}")

# Input form
with st.form("INPUT_FORM", clear_on_submit=True):
    user_input = st.text_input("Type a message", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Gemini is thinking..."):
        try:
            reply = get_gemini_response(user_input)
        except Exception as e:
            reply = f"Error: {e}"

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Rerun to display new messages
    st.rerun()
