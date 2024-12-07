import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

initialize_session_state()

# Add custom CSS for styling
st.markdown(
    """
    <style>
        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
        }
        .chat-message.assistant {
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        .chat-message.user {
            background-color: #e3f2fd;
            color: #1565c0;
        }
        footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
            padding: 10px 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main title

st.title("Speech to speech bot")
# Chat container
with st.container():
    st.markdown("<div class='chat-container' style='margin-top: -20px;'>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        role_class = "assistant" if message["role"] == "assistant" else "user"
        with st.chat_message(message["role"]):
            st.markdown(
                f"<div class='chat-message {role_class}'>{message['content']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# Footer container for input options
footer_container = st.container()
with footer_container:
    st.markdown("<footer>", unsafe_allow_html=True)
    audio_bytes = audio_recorder()
    st.markdown("</footer>", unsafe_allow_html=True)

if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.markdown(
            f"<div class='chat-message assistant'>{final_response}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

footer_container.float("bottom: 0rem;")