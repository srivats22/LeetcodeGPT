import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup as bs
import os
from common import llm_keys

genai.configure(api_key=llm_keys['Gemini'])
model = genai.GenerativeModel('gemini-1.5-flash')

def role_to_streamlit(role):
    if role == "model":
        return "assistant" 
    else:
        return role

def get_desc():
    if st.session_state.site_url != '':
        url_split = st.session_state.site_url.split('/')
        data = {
        "operationName":"questionData",
        "variables":{"titleSlug":url_split[4]},
        "query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

        r = requests.post('https://leetcode.com/graphql', json = data).json()
        soup = bs(r['data']['question']['content'], 'lxml')
        question =  soup.get_text().replace('\n',' ')
        st.session_state.problem_title = url_split[4]
        st.session_state.question = question
        st.session_state.llm_prompt = f'''You are an expert in leetcode problems. You are also an expert in
        {st.session_state.language}. You will help the you the user with any questions they might have
        related to {question}. You will also keep the following in check while answering:
        1. You will not write code until asked
        2. You will think carefully before answering the users question
        3. You will always answer exactly what the user asks for and nothing more.
        Once you are ready, reply with: I am ready to assist you with: {url_split[4]}'''
    else:
        st.write("Waiting for URL...")

def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role
    
def go_back():
    st.session_state.form_submitted = False
    st.session_state.all_variables_assigned = False
    
def ui():
    if "chat" not in st.session_state:
        print("Initializing chat...")
        get_desc()
        st. session_state.chat = model.start_chat(history = [])
        st.chat_message("user").markdown(st.session_state.llm_prompt)
        prompt_chat = st.session_state.chat.send_message(st.session_state.llm_prompt)
        st.chat_message("assistant").markdown(prompt_chat.text)
        print("Finished Initialzing...")
    
    with st.container():
        st.button("Go Back", on_click=go_back)
        st.title(f"Ask Gemini About: {st.session_state.problem_title}")

    for msg in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(msg.role)):
            st.markdown(msg.parts[0].text)

    if prompt := st.chat_input("Ask A Question"):
        st.chat_message("user").markdown(prompt)
        resp = st. session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(resp.text)