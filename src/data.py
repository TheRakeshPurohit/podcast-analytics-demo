from typing import List

import streamlit as st
from steamship import Tag

from src.utils import get_steamship_client

GUEST_TO_YOUTUBE_URL = {
    "Elon Musk": "https://youtu.be/ycPr5-27vSI",
}


@st.cache(ttl=3600, allow_output_mutation=True)
def load_guests():
    return {
        tag.name
        for tag in Tag.query(
            get_steamship_client(),
            space_id="B0D2A0F8-689E-42A2-87BF-7DF6AB0A83E4",
            tag_filter_query='kind "guest"',
        ).data.tags
    }


@st.cache(ttl=3600, allow_output_mutation=True)
def load_tags(guest: str) -> List[Tag]:
    return [
        tag
        for tag in Tag.query(
            get_steamship_client(),
            space_id="B0D2A0F8-689E-42A2-87BF-7DF6AB0A83E4",
            tag_filter_query=f'sameblock {{kind "guest" and name "{guest}"}}',
        ).data.tags
    ]


@st.cache(ttl=3600, allow_output_mutation=True)
def load_timestamp_tags():
    return sorted(list(dict({tag.start_idx: tag
                             for tag in Tag.query(get_steamship_client(), tag_filter_query='kind "timestamp"').data.tags
                             }).values()), key=lambda x: x.start_idx)
