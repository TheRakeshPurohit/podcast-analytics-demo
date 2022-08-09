import streamlit as st

from src.auth import check_auth
from src.data import load_timestamp_tags
from src.ui import select_guest
from src.utils import get_steamship_client

check_auth()

st.title("The Joe Rogan bible 📒")
st.text("Let's scan the brains of Joe Rogan's guests.")

guest, youtube_url, tags = select_guest()

search_query = st.text_input("Search query")

search_terms = [search_term.lower().strip() for search_term in search_query.split(" ") if search_term]

if search_terms:
    client = get_steamship_client()
    timestamp_tags = load_timestamp_tags()

    clips = []
    for ix, timestamp_tag in enumerate(timestamp_tags):
        if timestamp_tag.name.lower() == search_terms[0]:
            if sum(timestamp_tag.name.lower() in search_terms
                   for timestamp_tag in timestamp_tags[ix: ix + 10 + len(search_terms)]) == len(search_terms):
                start_time = int(float(timestamp_tags[ix].value["start_time"]))

                clips.append({
                    "video_url": f"{youtube_url}?t={start_time:.0f}",
                    "start_time": start_time,
                    "clip": " ".join([tag.name for tag in timestamp_tags[ix: ix + 10 + len(search_terms)]])
                }
                )

    for ix, clip in enumerate(sorted(clips, key=lambda x: x["start_time"])):
        st.markdown(f"#### Fragment {ix}")
        # st.markdown(clip["clip"])
        start_time = clip['start_time']
        st.video(data=f"{youtube_url}?t={start_time}", start_time=start_time)
