"""UI to browse podcast summaries."""
import streamlit as st
from steamship import Tag

from src.auth import authenticate, increase_usage
from src.data import fetch_youtube_url
from src.ui import footer, select_guest
from src.utils import get_steamship_client

st.title("The Joe Rogan Index 📒")
st.markdown("Get the insights of your favorite guests in 5 minutes instead of 3 hours.")

authenticate()

if increase_usage():
    selected_guest, file_ids = select_guest()

    episode_idx = st.radio(
        label="Episode", options=range(len(file_ids)), format_func=lambda x: f"Episode {x + 1}"
    )

    if episode_idx is not None:
        file_id = file_ids[episode_idx]
        youtube_url = fetch_youtube_url(file_id)

        topics = sorted(
            Tag.query(
                get_steamship_client(),
                tag_filter_query=f'blocktag and kind "topic_summary" and value("confidence") > 0.5'
                f'and samefile {{ file_id "{file_id}" }}',
            ).tags,
            key=lambda tag: -tag.value["confidence"],
        )
        topic_hashtags = " #".join([topic.name.split(">")[-1] for topic in topics])
        st.markdown(f"##### #{topic_hashtags}")

        chapters = sorted(
            Tag.query(
                get_steamship_client(),
                tag_filter_query=f'blocktag and kind "chapter" '
                f'and samefile {{ file_id "{file_id}" }}',
            ).tags,
            key=lambda x: int(x.name),
        )

        for chapter in chapters:
            st.markdown(f"## Chapter {chapter.name}: {chapter.value['gist']}")
            st.markdown(f"#### {chapter.value['headline']}")
            st.markdown(f"{chapter.value['summary']}")
            start = chapter.start_idx // 1000
            st.video(data=f"{youtube_url}?t={start:.0f}", start_time=start)

footer()
