import os
import streamlit as st

st.set_page_config(page_title=None,
                   page_icon=os.path.join("assets", "images", "logo-care.png"),
                   layout="wide",
                   initial_sidebar_state="collapsed",  # Hide sidebar by default
                   menu_items={"Get help": "mailto:amosb.dev@gmail.com | maigaabdoulaziz000@gmail.com",
                               "Report a Bug": "mailto:amosb.dev@gmail.com | maigaabdoulaziz000@gmail.com",
                               "About": None})
from streamlit_option_menu import option_menu
from page_format import default_pages_config, display_login_page, display_chat_page
from utils import is_logged_in

default_pages_config()

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
    
    .service-title{
        font-weight: bold;
    }
    
    .text-color-red{
        color: #A93031;
    }
    
    .text-color-blue-light{
        color: #8ED0F3;
    }
    
    ul.service-list > li {
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 2

# def streamlit_menu():
#
#     login_or_logout = "Login" if not is_logged_in() else "Logout"
#     menu_options = ["Services", "Partnership", "Donate", "Pricing", login_or_logout, "Get Started", "Chat"]
#
#     if is_logged_in():
#         menu_options = [item for item in menu_options if item != "Get Started"]
#
#     # if example == 2:
#     # 2. horizontal menu w/o custom style
#     selected = option_menu(
#         menu_title=None,  # required
#         options=menu_options,  # required
#         # icons=["house", "book", "envelope", "house", "book", "envelope"],  # optional
#         # menu_icon="cast",  # optional
#         manual_select=0,  # optional
#         orientation="horizontal",
#         styles="width: 100%;"
#     )
#     return selected


menu_row_cols = st.columns([1, 9])

# Logo
menu_row_cols[0].image(image=os.path.join("assets", "images", "logo-care-mini.png"), width=70)

with menu_row_cols[1]:
    login_or_logout = "Login" if not is_logged_in() else "Logout"
    menu_options = ["Services", "Partnership", "Donate", "Pricing", login_or_logout, "Get Started", "Chat"]

    if is_logged_in():
        menu_options = [item for item in menu_options if item != "Get Started"]

    # if example == 2:
    # 2. horizontal menu w/o custom style
    selected = option_menu(
        menu_title=None,  # required
        options=menu_options,  # required
        # icons=["house", "book", "envelope", "house", "book", "envelope"],  # optional
        # menu_icon="cast",  # optional
        manual_select=0,  # optional
        orientation="horizontal",
        styles="width: 100%;"
    )

    st.session_state["selected_menu"] = selected
    # selected = streamlit_menu()

# Create two columns
col1, col2 = st.columns([2, 1])

if selected == "Services":
    # Display text in the second column
    with col1:
        st.markdown("""
        <h2 class="service-title"><span class="text-color-red">Your</span> <span class="text-color-blue-light">Health</span>, <span class="text-color-red">Your</span> <span class="text-color-blue-light">Privacy</span>, <span class="text-color-red">Your</span> <span class="text-color-blue-light">Future</span></h2>
        
        <ul class="service-list">
            <li>Instant answers and expert care for your sexual health questions.</li>
            <li>Start with our intelligent ChatBot for quick, reliable information.</li>
            <li>Then, connect anonymously with qualified doctors for personalized guidance.</li>
            <li>No judgment, no waiting rooms - just the care you need, when you need it.</li>
            <li>Take control of your sexual health journey today.</li>
        </ul>

        """, unsafe_allow_html=True)

    # Display the image in the first column
    with col2:
        st.image(image=os.path.join("assets", "images", "img2.png"))

if selected == "Partnership":
    st.title(f"You have selected {selected}")
if selected == "Donate":
    st.title(f"You have selected {selected}")
if selected == "Pricing":
    st.title(f"You have selected {selected}")
if selected in ["Login", "Logout"]:
    display_login_page()
if selected == "Chat":
    info_row = st.columns([1, 1, 1])
    if is_logged_in():
        info_row[1].success("All your conversation are anonymous")

        chat_tab_row = st.columns([1, 5, 1])

        chat_type_tabs = chat_tab_row[1].tabs(["Chat Bot", "Talk to a Doctor"])

        with chat_type_tabs[0]:
            st.info(
                "You are talking with our system, not a human. All your conversations are private and accessible by you only")
            display_chat_page()
        with chat_type_tabs[1]:
            st.warning("You will talk with a Doctor. A human.")

    else:

        info_row[1].error("You need to login to use the chat bot.")
        info_row[1].info("Go to the login tab to log in.")
