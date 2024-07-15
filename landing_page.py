import streamlit as st
import os
from common import llm_keys

def validate_form():
    if llm_keys[st.session_state.llm_model_selection] == '':
        st.error(f"{st.session_state.llm_model_selection} API Key is missing. Please configure it in common.py and rerun the application, or choose a different model.")
        return  # Early return to prevent further execution if validation fails

    if st.session_state.site_url == "":
        st.error("Please provide a valid Site URL.")
        return

    # Validation successful, set flags and rerun
    st.session_state.form_submitted = True
    st.session_state.all_variables_assigned = True
    st.rerun()

def show_form():
    program_lang_tuple = ('Java', 'Dart', 'Go', 'Python', 'Kotlin')
    st.title("Form Page")
    
    with st.form(key='my_form'):
        st.session_state.site_url = st.text_input(
            label="Enter/Paste Leetcode Problem URL",
            placeholder="Ex: https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/description/",
        )

        st.session_state.language = st.selectbox(
            'Choose A Programming Language',
            program_lang_tuple
        )

        st.session_state.llm_model_selection = st.selectbox(
            'Choose An LLM',
            ("Gemini", "Chat GPT")
        )

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            validate_form()