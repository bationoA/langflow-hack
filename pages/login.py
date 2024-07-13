import os.path
import streamlit as st
from db_handler import init_database


from utils import authorize_login, is_logged_in, logout

init_database()

logo_row = st.columns([2, 1, 2])
logo_row[1].image(image=os.path.join("assets", "images", "logo-care.png"), width=100)

page_title = "TrustNode Health"
st.markdown(f"<h1 style='text-align:center; color: gray'>{page_title}</h1>",
            unsafe_allow_html=True)


if not is_logged_in():
    with st.form("login-form"):
        st.write("Login")
        username = st.text_input(label="username")
        password = st.text_input(label="password", type="password")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            login_status = authorize_login(usern=username, passw=password)

            if not login_status:
                st.error("The username or password is incorrect")
            else:
                st.session_state["is_logged_in"] = True
                st.success("You are now authenticated!")
                st.page_link(label="Continue", page=os.path.join("pages", "chat.py"))
else:
    st.write("You're already logged in")
    st.button(label="Sign out", on_click=logout)


print(f"is_logged_in: {is_logged_in()}")
