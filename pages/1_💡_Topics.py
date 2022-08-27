from collections import defaultdict

import streamlit as st

from src.auth import check_auth
from src.ui import footer, select_topic, list_clips_for_topics

check_auth()

st.title("The Joe Rogan bible 📒")
st.markdown("Let's find out what Joe Rogan's guests say about your favorite topics.")

topic, files = select_topic()

guest_to_file = defaultdict(list)
for file in files:
    guest_tags = [tag for tag in file.tags if tag.kind == "guest"]
    if guest_tags:
        guest_to_file[guest_tags[0].name].append(file)

selected_guest = st.radio("Guest", options=guest_to_file)

if selected_guest:
    for file in guest_to_file[selected_guest]:
        tags = file.blocks[0].tags
        youtube_url = [tag.name for tag in file.tags if tag.kind == "youtube_url"][0]
        list_clips_for_topics(youtube_url, [topic], tags, selected_guest)

footer()
