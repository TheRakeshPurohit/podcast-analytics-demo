from steamship import Steamship
import streamlit as st


def get_steamship_client() -> Steamship:
    return Steamship(
        api_key=st.secrets["steamship_api_key_audio"],
        api_base="https://api.steamship.com/api/v1/",
        app_base="https://steamship.run/",
        web_base="https://app.steamship.com/"
    )
