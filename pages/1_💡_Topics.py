"""UI to browse podcast episodes by topic."""

import streamlit as st

from src.auth import authenticate, increase_usage
from src.data import select_guests_by_topic
from src.ui import footer, list_clips_for_topics, select_topic

st.title("The Joe Rogan Index 📒")
st.markdown("Let's find out what Joe Rogan's guests say about your favorite topics.")

authenticate()

if increase_usage():
    selected_topic = select_topic()

    selected_guest = st.selectbox("Guest", options=select_guests_by_topic(selected_topic))

    if selected_guest:
        list_clips_for_topics(selected_topic, selected_guest)

footer()
