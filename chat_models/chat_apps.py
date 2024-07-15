import streamlit as st
from chat_models.gemini_chat import ui as gemini
from chat_models.chatgpt_chat import ui as chatGpt

def choose_app():
    if st.session_state.llm_model_selection == "Gemini":
        gemini()
    if st.session_state.llm_model_selection == "Chat GPT":
        chatGpt()