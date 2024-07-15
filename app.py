import streamlit as st
from landing_page import show_form
from chat_models.gemini_chat import ui
from chat_models import chat_apps
from common import llm_keys

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'all_variables_assigned' not in st.session_state:
    st.session_state.all_variables_assigned = False
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

st.set_page_config(
    page_title="LeetcodeGPT"
)

if st.session_state.form_submitted and st.session_state.all_variables_assigned:
    chat_apps.choose_app()
else:
    show_form()