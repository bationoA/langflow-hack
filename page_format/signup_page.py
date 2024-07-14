from datetime import datetime

import streamlit as st

from db_handler import DatabaseHandler
from flow import get_flow1_response
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


def display_signup_page():
    st.session_state['ui-text'] = {}

    st.session_state['ui-text']['how_can_i_help_with_tourism_benin'] = "How can I help you?"
    st.session_state['ui-text']['a_moment_please'] = "A moment please"

    container = st.container(height=1000, border=False)
    container_cols = container.columns([1, 5, 1])
    with container_cols[1]:

        if is_logged_in():
            st.info("You're currently logged in. You need to log out in order to create an account")
        else:  # Creation of an account
            account_type_tab = st.tabs(["I want to seek for medical advices", "I am Doctor"])

            values_considered_invalid = ["", None]

            with account_type_tab[0]:
                with st.form(key="service-seeker-form"):
                    st.info(
                        "You will be able to anonymously receive guidance from both and trained AI and a human doctor")
                    user_name = st.text_input(label="choose a user name. This should NOT be your real name")
                    password = st.text_input(label="choose a password", type="password")
                    submit_service_seeker = st.form_submit_button("submit")

                    if submit_service_seeker:
                        user_type = "service-seeker"
                        if user_name in values_considered_invalid or password in values_considered_invalid:
                            st.error("Error: user_name and password must be provided")
                        else:
                            data = {
                                "username": user_name,
                                "password": password,
                                "user_type": user_type,
                                "joined_at": datetime.utcnow().isoformat()
                            }
                            # Insert into a database
                            db_handler = DatabaseHandler()
                            result = db_handler.insert_data_into_table(table_name="user", data=data)

                            if result:
                                st.success("You have successfully signed up. You can now take benefit of the advance "
                                           "chat feature of the platform after logging in using your credentials.")

            with account_type_tab[1]:
                with st.form(key="form-form"):
                    st.info("After approval, you'll will provide service to people seeking for medical advice. You "
                            "are Not anonymous")
                    st.warning("You will be asked to provide further information for approval")
                    user_name = st.text_input(label="choose a user name. This should NOT be your real name")
                    password = st.text_input(label="choose a password", type="password")
                    title = st.text_input(label="Your professional title")
                    first_name = st.text_input(label="Enter you first name")
                    last_name = st.text_input(label="Enter you last name")
                    bio_expertise = st.text_input(label="Bio and Area of expertise")

                    submit_doctor = st.form_submit_button("submit")

                    if submit_doctor:
                        user_type = "doctor"
                        if user_name in values_considered_invalid or password in values_considered_invalid or \
                                title in values_considered_invalid or first_name in values_considered_invalid or \
                                last_name in values_considered_invalid or bio_expertise in values_considered_invalid:
                            st.error("Error: All field must be provided")
                        else:
                            # Insert into a database
                            data = {
                                "username": user_name,
                                "password": password,
                                "title": title,
                                "firstname": first_name,
                                "lastname": last_name,
                                "bio": bio_expertise,
                                "user_type": user_type,
                                "joined_at": datetime.utcnow().isoformat()
                            }
                            # Insert into a database
                            db_handler = DatabaseHandler()
                            result = db_handler.insert_data_into_table(table_name="user", data=data)

                            if result:
                                st.success("You have successfully signed up. You can now logging in using your credentials.")
                                st.warning("You account will be activated after further verification for approval. Expect further information request from us with 2 to 3 days.")
