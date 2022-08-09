import streamlit as st

from src.auth import check_auth
from src.ui import STYLED_SENTIMENTS, list_clips_for_topics, select_guest

check_auth()

st.title("The Joe Rogan bible 📒")
st.markdown("Let's see what Joe Rogan's guests feel sad or happy about.")

guest, youtube_url, tags = select_guest()

sentiments = {tag.name for tag in tags if tag.kind == "sentiments"}
selected_sentiment = st.selectbox(
    "Sentiment", options=sentiments, format_func=lambda x: STYLED_SENTIMENTS[x]
)

name_tags = []
for sentiment_tag in dict(
    sorted(
        {
            tag.start_idx: tag
            for tag in tags
            if tag.kind == "sentiments" and tag.name in selected_sentiment
        }.items(),
        key=lambda x: x,
    )
).values():
    name_tags.extend(
        [
            tag
            for tag in tags
            if tag.kind == "names"
            and tag.start_idx >= sentiment_tag.start_idx
            and tag.end_idx <= sentiment_tag.end_idx
        ]
    )

st.write(
    f"{guest.title()} feels {STYLED_SENTIMENTS[selected_sentiment]} about the following topics:"
)

st.write("- " + "\n - ".join({tag.value["value"] for tag in name_tags}))
list_clips_for_topics(youtube_url, name_tags, tags)
