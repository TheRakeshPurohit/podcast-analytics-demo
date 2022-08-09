import streamlit as st

from src.auth import check_auth
from src.ui import select_guest, list_clips_for_topics

check_auth()

st.title("The Joe Rogan bible 📒")
st.markdown("Let's find out what Joe Rogan's guests say about specific topics.")

guest, youtube_url, tags = select_guest()

names = {tag.value["value"] for tag in tags if tag.kind == "names"}
selected_names = st.multiselect("Topic", options=names)

if selected_names:
    list_clips_for_topics(youtube_url, selected_names, tags)
