import streamlit as st


def check_auth() -> None:
    password = st.sidebar.text_input(label="Password", type="password")
    if password != "LetTheMagicBegin":
        st.stop()
