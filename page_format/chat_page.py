import streamlit as st

from flow import get_flow_response
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

    .container-xxl {
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

    section.main > div.block-container {
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


def display_chat_page():
    if not is_logged_in():
        redirect_to("")

    st.session_state['ui-text'] = {}

    st.session_state['ui-text']['how_can_i_help_with_tourism_benin'] = "How can I help you?"
    st.session_state['ui-text']['a_moment_please'] = "A moment please"

    container = st.container(height=450, border=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with container.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # prompt = st.session_state['prompt'] if "prompt" in st.session_state else None

    # React to user input
    if prompt := st.chat_input(f"{st.session_state['ui-text']['how_can_i_help_with_tourism_benin']}?"):
        # Display user message in chat message container
        container.chat_message("user").markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Collect user's query
        # pipeline.user_query = prompt
        with container:
            with st.spinner(f"{st.session_state['ui-text']['a_moment_please']}..."):
                # pipeline.run()
                response = get_flow_response(user_message=prompt)
                # try:
                #     response = get_flow_response(user_message=prompt)
                # except BaseException as e:
                #     response = str(e)


        # response = f"Echo: {prompt}"
        #     response = format_article_display(pipeline.paragraphs) if len(pipeline.paragraphs) \
        # else f"""<p style="background-colr: white; color: red">Connection Error: Check your internet, OpenAI API key or try later.</p>"""

        # response = f"""<p style="background-colr: white; color: red">Connection Error: Check your internet, OpenAI API key or try later.</p>"""

        # Display assistant response in chat message container
        with container.chat_message("assistant"):
            st.markdown(response, unsafe_allow_html=True)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

