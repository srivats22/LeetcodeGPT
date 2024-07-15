from openai import OpenAI
import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
from common import llm_keys

client = OpenAI(api_key=llm_keys['Chat GPT'])

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

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def chat_model(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

def ui():
    if "chat" not in st.session_state:
        print("Initializing chat...")
        get_desc()
        chat_model(st.session_state.llm_prompt)
        print("Finished Initialzing...")
    
    with st.container():
        st.title(f"Ask ChatGPT About: {st.session_state.problem_title}")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask A Question"):
        chat_model(prompt)