from concurrent.futures import ThreadPoolExecutor
from itertools import groupby

import streamlit as st
from steamship import Tag, File

from src.utils import get_steamship_client


@st.cache(ttl=3600, allow_output_mutation=True)
def load_guests():
    return [
        tag
        for tag in Tag.query(
            get_steamship_client(),
            tag_filter_query='filetag and kind "guest" and samefile {kind "entities"}',
        ).data.tags
    ]


@st.cache(ttl=3600, allow_output_mutation=True)
def load_topics():
    topics = Tag.query(
        get_steamship_client(),
        tag_filter_query='blocktag and kind "entities" and samefile {filetag and kind "guest"}',
    ).data.tags

    filtered_topics = [
        topic
        for topic in topics
        if topic.name not in ("email_address", "person_age", "url", "time", "money_amount")
    ]

    with ThreadPoolExecutor(max_workers=8) as executor:
        for file_id in {tag.file_id for tag in topics}:
            executor.submit(load_file, file_id)

    return dict(
        sorted(
            {
                k: {tag.file_id for tag in v}
                for k, v in groupby(
                sorted(filtered_topics, key=lambda x: x.value["value"].lower()),
                lambda x: x.value["value"].lower(),
            )
            }.items(),
            key=lambda x: -len(x[1]),
        )
    )


@st.cache(ttl=3600, allow_output_mutation=True)
def load_file(file_id: str) -> File:
    return File.get(get_steamship_client(), file_id).data
