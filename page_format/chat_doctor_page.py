import json
import os.path

import streamlit as st

from flow import get_flow2_response
from utils import is_logged_in, redirect_to

st.markdown("""
<style>
    .st-emotion-cache-13ln4jf{
        width: 100%;
        padding: 6rem 1rem 10rem;
        padding-right: 1rem;
        padding-left: 1rem;
        max-width: 100%
    }

    .st-emotion-cache-1tsdzql {
      width: 1680px;
      position: relative;
      margin-top: -.65rem;
    }

    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        -moz-box-flex: 1;
        flex-grow: 1;
        -moz-box-align: stretch;
        align-items: stretch;
        gap: 1rem;
        margin-left: 190px;
        margin-right: 190px;
    }

    .container_doct-xxl {
        background-color: white;
        border-radius: .5rem;
    }


    div.stChatInput textarea{
        min-height: 4rem;
        max-height: 4rem;
        font-size: 2.2rem;
    }

    div.stChatInput button{
        width: 5rem;
        height: 100%;
    }

    div.stChatInput button svg{
        width: 100%;
        height: 100%;
    }

    .st-emotion-cache-1uj96rm{
        width: 55%;
    }

    section.main > div.block-container_doct {
      padding: 0rem 5rem 5rem 10rem;
    }


    .text-color-1{
        color: black;
        weight: bold;
    }

    div.stPageLink a{
        border: 1px solid blue;
    }

    div.stPageLink span p{
        color: black;
        font-size:2rem;
        weight: bold;
    }




</style>

""", unsafe_allow_html=True)


def display_chat_doctor_page():
    """
    Display chat area with a human doctor.

    :return:
    """
    if not is_logged_in():
        redirect_to("")

    pre_prompt = """"
    You're a useful assistant that comes at the end of a discussion between a patient and a doctor.
    The user will ask you to perform some tasks that might include summary and more. 
    Never take position for either the user of the doctor. 
    Never saying or suggest something that goes against what the doctor has said during the conversation.
    In doubt, always suggest the user book another consultation session with the doctor for more clarity or to with another doctor to have an additional point of view.

    This is the pass conversation of the user with the doctor
    context: {context}
    User: {user_input}
    """

    st.session_state['ui-text'] = {}

    st.session_state['ui-text']['how_can_i_help_with_tourism_benin'] = "How can I help you?"
    st.session_state['ui-text']['a_moment_please'] = "A moment please"

    container_doct = st.container(height=450, border=True)


    # Initialize chat history
    if "doctor_messages" not in st.session_state:
        # Get sample discussion with a doctor
        with open(os.path.join("database", "doctor_sample_chat.json"), "r") as f:
            st.session_state.doctor_conversation_only = json.loads(f.read())

        st.session_state.doctor_messages = st.session_state.doctor_conversation_only.copy()

    # Display chat messages from history on app rerun
    for message in st.session_state.doctor_messages:
        avatar = None if message["role"] != "doctor" else os.path.join("assets", "images", "doctor_jane_avatar.png")
        with container_doct.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"], unsafe_allow_html=True)

    pre_prompt = pre_prompt.replace("{context}", json.dumps(st.session_state.doctor_conversation_only))

    # prompt = st.session_state['prompt'] if "prompt" in st.session_state else None

    # React to user input
    if prompt := st.chat_input(f"{st.session_state['ui-text']['how_can_i_help_with_tourism_benin']}?",
                               key="chat_doctor"):
        # Display user message in chat message container_doct
        container_doct.chat_message("user").markdown(prompt)

        # Add user message to chat history
        st.session_state.doctor_messages.append({"role": "user", "content": prompt})

        # Collect user's query
        # pipeline.user_query = prompt
        with container_doct:
            with st.spinner(f"{st.session_state['ui-text']['a_moment_please']}..."):
                print("user input---{}: ".format(prompt))
                print("prompt---{}: ".format(pre_prompt.replace("{user_input}", prompt)))

                response = get_flow2_response(user_message=pre_prompt.replace("{user_input}", prompt))
                response = dict(response[0].outputs[0].results["message"])["text"]
                # try:
                #     response = get_flow_response(user_message=prompt)
                # except BaseException as e:
                #     response = str(e)

        # Display assistant response in chat message container_doct
        with container_doct.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        # Add assistant response to chat history

        st.session_state.doctor_messages.append({"role": "assistant", "content": response})
