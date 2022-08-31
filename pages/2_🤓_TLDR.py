"""UI to browse podcast summaries."""
import streamlit as st

from src.auth import authenticate, increase_usage
from src.ui import footer, select_guest

st.title("The Joe Rogan bible 📒")
st.markdown("Get the insights of your favorite guests in 5 minutes instead of 3 hours.")

authenticate()

if not increase_usage():
    st.error(
        "Usage quota exceeded, [contact support](mailto:developers@steamship.com) for more credits."
    )
    st.stop()

guest, youtube_url, tags = select_guest()

topics = sorted(
    [tag for tag in tags if tag.kind == "topic_summary"], key=lambda tag: -tag.value["relevance"]
)

chapters = [tag for tag in tags if tag.kind == "chapter"]

topic_hashtags = " #".join(
    [topic.name.split(">")[-1] for topic in topics if topic.value["relevance"] > 0.5]
)
st.markdown(f"##### #{topic_hashtags}")

for chapter in chapters:
    st.markdown(f"## Chapter {chapter.name}: {chapter.value['gist']}")
    st.markdown(f"#### {chapter.value['gist']}")
    st.markdown(f"{chapter.value['summary']}")
    start = chapter.start_idx // 1000
    st.video(data=f"{youtube_url}?t={start:.0f}", start_time=start)

footer()
