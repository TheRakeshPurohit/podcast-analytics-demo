"""Helper functions to load and store data."""
from itertools import groupby
from typing import List

import streamlit as st
from steamship import Tag

from src.utils import get_steamship_client


@st.cache(ttl=3600)
def load_guest_tags() -> List[Tag]:
    """Load the guests that appeared on the podcast."""
    return Tag.query(
        get_steamship_client(),
        tag_filter_query='filetag and kind "guest" and samefile {kind "entities"}',
    ).data.tags


@st.cache(ttl=3600)
def select_guests_by_topic(topic: str) -> List[str]:
    return [tag.name for tag in Tag.query(
        get_steamship_client(),
        tag_filter_query=f'filetag and kind "guest" '
                         f'and samefile {{blocktag and kind "entities" '
                         f'         and ( value("value") = "{topic}" or value("value") = "{topic.lower()}" ) }}',
    ).data.tags]


@st.cache(ttl=3600)
def load_topics() -> List[str]:
    """Load the topics mentioned on the podcasts."""
    topics = Tag.query(
        get_steamship_client(),
        tag_filter_query='blocktag and kind "entities" and samefile {filetag and kind "guest"}',
    ).data.tags

    filtered_topics = [
        topic
        for topic in topics
        if topic.name not in ("email_address", "person_age", "url", "time", "money_amount")
    ]

    return [k.title() for k, v in
            sorted(
                {
                    k: {tag.file_id for tag in v}
                    for k, v in groupby(
                    sorted(filtered_topics, key=lambda x: x.value["value"].lower()),
                    lambda x: x.value["value"].lower(),
                )
                }.items(),
                key=lambda x: -len(x[1]),
            )]


@st.cache(ttl=3600)
def get_entity_tags_by_topic(selected_topic: str, selected_speaker: str):
    return Tag.query(
        get_steamship_client(),
        tag_filter_query=f'blocktag and kind "entities" '
                         f'and ( value(\"value\") = \"{selected_topic}\" or name \"{selected_topic}\" '
                         f'or value(\"value\") = \"{selected_topic.lower()}\" or name \"{selected_topic.lower()}\" ) '
                         f'and samefile {{ filetag and kind \"guest\" and name \"{selected_speaker}\"}}',
    ).data.tags


@st.cache(ttl=3600)
def fetch_youtube_url(file_id: str):
    return Tag.query(
        get_steamship_client(),
        tag_filter_query=f'filetag and kind "youtube_url" and samefile {{ file_id "{file_id}" }}'
    ).data.tags[0].name
