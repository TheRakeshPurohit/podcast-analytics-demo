"""Helper functions to load and store data."""
from itertools import groupby
from typing import List, Dict, Set

import streamlit as st
from steamship import Tag

from src.utils import get_steamship_client


@st.cache(ttl=3600)
def load_guest_tags() -> Dict[str, Set[str]]:
    """Load the guests that appeared on the podcast."""
    guest_tags = Tag.query(
        get_steamship_client(),
        tag_filter_query='filetag and kind "guest"',
    ).data.tags

    return {k: {x.file_id for x in v} for k, v in
            groupby(sorted(guest_tags, key=lambda x: x.name), key=lambda x: x.name)}


@st.cache(ttl=3600)
def select_guests_by_topic(selected_topic: str) -> List[str]:
    return [tag.name for tag in Tag.query(
        get_steamship_client(),
        tag_filter_query=f'filetag and kind "guest" '
                         f'and samefile {{ '
                         f'     name "{selected_topic}" '
                         f'     or name "{selected_topic.lower()}" '
                         f'     or name "{selected_topic.upper()}" '
                         f'     or name "{selected_topic.capitalize()}" '
                         f'}}',
    ).data.tags]


@st.cache(ttl=3600)
def load_topics() -> List[str]:
    """Load the topics mentioned on the podcasts."""
    entity_tags = Tag.query(
        get_steamship_client(),
        tag_filter_query='blocktag and kind "entity"',
    ).data.tags

    filtered_entity_tags = [
        topic
        for topic in entity_tags
        if topic.value["type"] not in ("email_address", "person_age", "url", "time", "money_amount")
    ]

    return [k.title() for k, v in
            sorted(
                {
                    k: {tag.file_id for tag in v}
                    for k, v in groupby(
                    sorted(filtered_entity_tags, key=lambda x: x.name.lower()),
                    lambda x: x.name.lower(),
                )
                }.items(),
                key=lambda x: -len(x[1]),
            )]


@st.cache(ttl=3600)
def get_entity_tags_by_topic(selected_topic: str, selected_speaker: str) -> List[Tag]:
    return Tag.query(
        get_steamship_client(),
        tag_filter_query=f'blocktag '
                         f'and (name "{selected_topic}" '
                         f'     or name "{selected_topic.lower()}" '
                         f'     or name "{selected_topic.upper()}" '
                         f'     or name "{selected_topic.capitalize()}" ) '
                         f'and samefile {{ filetag and kind "guest" and name "{selected_speaker}"}}',
    ).data.tags


@st.cache(ttl=3600)
def fetch_youtube_url(file_id: str):
    return Tag.query(
        get_steamship_client(),
        tag_filter_query=f'filetag and kind "youtube_url" and samefile {{ file_id "{file_id}" }}'
    ).data.tags[0].name
