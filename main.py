import os
import streamlit as st
from db_handler import init_database
from page_format import default_pages_config
from utils import is_logged_in, logout

init_database()

# --------------------- LOGO-TEXT AND TITLE
app_title = "TrustNode Health"
page_title = "AI-driven Tool for Record linkage in HDSS communities Within the INSPIRE Network"
page_description = "By Amos Bationo and Abdoul Aziz Maiga - Team <b><i>Unfold</i></b>"

# default_pages_config(_title=page_title)

menu_cols = st.columns([4, 1, 1, 1, 2, 1, 1])

menu_cols[0].image(image=os.path.join("assets", "images", "logo-care.png"), width=100)

menu_cols[1].button("Services")
menu_cols[2].button("Partnership")
menu_cols[3].button("Donate")
menu_cols[4].button("Pricing")
if not is_logged_in():
    menu_cols[5].page_link(label="Sign in", page=os.path.join("pages", "login.py"))
    menu_cols[6].button("Get Started")
else:
    menu_cols[5].button(label="Sign out", on_click=logout)
