"""Collection of helper functions to explore insights from the podcast."""
from steamship import Steamship


def get_steamship_client() -> Steamship:
    """Connect to the production steamship."""
    return Steamship(
        api_key="86F32988-D2B5-4C8B-8DA4-22B7CD1BB2D8",
        api_base="https://api.steamship.com/api/v1/",
        app_base="https://steamship.run/",
        web_base="https://app.steamship.com",
        workspace="podcasts"
    )
