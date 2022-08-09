import streamlit as st

from src.auth import check_auth

st.set_page_config(page_title="The Joe Rogan Bible  📒", page_icon="📒", layout="centered")

check_auth()
st.title("The Joe Rogan Bible 📒")
st.markdown("### 👈 Click one of the links in the sidebar to get started.")

hide_streamlit_style = """
            <style>

footer {
	visibility: hidden;
	}
footer:after {
	content:'Made with ❤️ on Steamship';
	color: rgba(0,0,0,1);
	visibility: visible;
	display: block;
	position: relative;
	padding: 5px;
	top: 2px;
}
            </style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
