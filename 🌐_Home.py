import streamlit as st

from src.auth import check_auth
from src.ui import footer

st.set_page_config(page_title="The Joe Rogan Bible  📒", page_icon="📒", layout="centered")

check_auth()
st.title("The Joe Rogan Bible 📒")
st.markdown("### 👈 Click one of the links in the sidebar to get started.")

footer()
