import streamlit as st

from src.auth import check_auth
from src.ui import footer, select_guest

check_auth()

st.title("The Joe Rogan bible 📒")
st.markdown("Let's see what Joe Rogan's guests feel sad or happy about.")

guest, youtube_url, tags = select_guest()

topics = sorted([tag for tag in tags if tag.kind == "topic_summary"],
                key=lambda tag: -tag.value["relevance"])

chapters = [tag for tag in tags if tag.kind == "chapter"]

topic_hashtags = " #".join([topic.name.split(">")[-1] for topic in topics if topic.value["relevance"] > .5])
st.markdown(f"##### #{topic_hashtags}")

for chapter in chapters:
    st.markdown(f"## Chapter {chapter.name}: {chapter.value['gist']}")
    st.markdown(f"#### {chapter.value['gist']}")
    st.markdown(f"{chapter.value['summary']}")
    start = chapter.start_idx // 1000
    st.video(data=f"{youtube_url}?t={start:.0f}", start_time=start)

footer()
