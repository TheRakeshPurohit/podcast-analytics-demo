from pathlib import Path

import streamlit as st

from src.auth import authenticate
from src.ui import footer

st.set_page_config(page_title="The Joe Rogan Bible  📒",
                   page_icon=Path("data/logo.png").open("rb").read(),
                   layout="centered")
footer()

authenticate()
st.title("The Joe Rogan Bible 📒")
st.markdown("### 👈 Click one of the links in the sidebar to get started.")

footer()
