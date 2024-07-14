import os.path
import streamlit as st
from db_handler import init_database

from utils import authorize_login, is_logged_in, logout, redirect_to

init_database()


def display_login_page():

    page_title = "Login" if not is_logged_in() else "Logout"
    st.markdown(f"<h1 style='text-align:center; color: gray'>{page_title}</h1>",
                unsafe_allow_html=True)

    login_form_cols = st.columns([3, 4, 3])

    if not is_logged_in():
        with login_form_cols[1].form("login-form"):
            username = st.text_input(label="username", key="username")
            password = st.text_input(label="password", type="password")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted and username != "" and password != "":
                login_status = authorize_login(usern=username, passw=password)

                if not login_status:
                    st.error("The username or password is incorrect")
                else:
                    # redirect_to(url="")
                    st.success("You are now logged in!")
                    # st.page_link(label="Continue", page=os.path.join("Streamlit_app.py"))
            elif submitted:
                st.error("username and password must be provided")

    else:
        login_form_cols[1].warning("Click below to log out")
        login_form_cols[1].button(label="Logout", on_click=logout)

