"""Collection of helper functions to explore insights from the podcast."""
import streamlit as st
from steamship import Steamship


def get_steamship_client() -> Steamship:
    """Connect to the production steamship."""
    return Steamship(
        api_key=st.secrets["steamship_api_key"],
        api_base="https://api.staging.steamship.com/api/v1/",
        app_base="https://apps.staging.steamship.com/",
        web_base="https://app.staging.steamship.com",
    )
