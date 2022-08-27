import streamlit as st
from steamship import Steamship


def get_steamship_client() -> Steamship:
    return Steamship(
        api_key=st.secrets["steamship_api_key"],
        api_base="https://api.staging.steamship.com/api/v1/",
        app_base="https://apps.staging.steamship.com/",
        web_base="https://app.staging.steamship.com",
    )
