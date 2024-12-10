import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

st.set_page_config(page_title="Chatbot Dummy", page_icon=":speech_balloon:")
st.title("Chatbot Dummy")
st.caption("This is a dummy chatbot.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generate response
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )
            response_placeholder = st.empty()
            full_response = ""

            # Collect the streamed response
            for chunk in stream:
                if content := chunk.choices[0].delta.content:
                    full_response += content
                    response_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
