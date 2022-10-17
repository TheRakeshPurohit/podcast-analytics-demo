"""Collection of helper functions to explore insights from the podcast."""
import streamlit as st
from steamship import Steamship


def get_steamship_client() -> Steamship:
    """Connect to the production steamship."""
    return Steamship(
        api_key=st.secrets["steamship_api_key"],
        api_base="https://api.steamship.com/api/v1/",
        app_base="https://steamship.run/",
        web_base="https://app.steamship.com",
        workspace="podcasts"
    )
