from collections import defaultdict, Counter
from typing import List, Union

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from steamship import Tag

from src.data import load_tags, load_guests

STYLED_EMOTIONS = {
    "happiness": "Happy 😁",
    "anger": "Angry 😡",
    "unknown": "Not sure 🤧"
}

STYLED_SENTIMENTS = {
    "POS": "Positive 👍",
    "NEG": "Negative 👎",
    "NEUTRAL": "Neutral 🇨🇭"
}

STYLED_TAGS = {
    "emotions": STYLED_EMOTIONS,
    "sentiments": STYLED_SENTIMENTS
}


def select_guest():
    guests = load_guests()

    guest = st.selectbox("Guest", options=guests)
    if not guest:
        st.markdown("Please select a guest.")
    else:
        tags = load_tags(guest)
        youtube_url = [tag.name for tag in tags if tag.kind == "youtube_url"][0]
        return guest, youtube_url, tags


def list_clips_for_topics(youtube_url: str, selected_names: Union[List[str], List[Tag]], tags: List[Tag]) -> None:
    global_aggregated_tags = defaultdict(Counter)

    if isinstance(selected_names, list) and len(selected_names) > 0 and isinstance(selected_names[0], str):
        selected_names = dict(sorted({
                                         tag.start_idx: tag
                                         for tag in tags if
                                         tag.kind == "names" and tag.value["value"] in selected_names
                                     }.items(), key=lambda x: x)).values()

    clips = []
    for name_tag in selected_names:
        timestamp_tags = sorted([
            tag
            for tag in tags
            if tag.kind == "timestamp"
               and tag.start_idx >= name_tag.start_idx
               and tag.end_idx <= name_tag.end_idx
        ], key=lambda x: float(x.value.get("start_time", 1_000_000) or 1_000_000))
        aggregated_overlapping_tags = defaultdict(list)

        for tag in [
            tag
            for tag in tags
            if tag.kind not in {"names", "article-topics", "timestamp"}
            if (tag.start_idx is None or tag.start_idx <= name_tag.start_idx + len(name_tag.name))
               and (tag.end_idx is None or tag.end_idx >= name_tag.end_idx - len(name_tag.name))
        ]:
            aggregated_overlapping_tags[tag.kind].append(
                STYLED_TAGS.get(tag.kind, {}).get(tag.name, tag.name)
            )

        if "emotions" not in aggregated_overlapping_tags:
            aggregated_overlapping_tags["emotions"].append(STYLED_EMOTIONS["unknown"])

        if "sentiments" not in aggregated_overlapping_tags:
            aggregated_overlapping_tags["sentiments"].append(STYLED_SENTIMENTS["NEUTRAL"])

        if "speaker" not in aggregated_overlapping_tags:
            aggregated_overlapping_tags["speaker"].append("unkown")

        for tag_kind in ("emotions", "sentiments", "speaker"):
            global_aggregated_tags[tag_kind].update(aggregated_overlapping_tags[tag_kind])

        if timestamp_tags:
            start_time = float(timestamp_tags[0].value["start_time"])

            emotion = aggregated_overlapping_tags['emotions'][0]
            sentiment = aggregated_overlapping_tags['sentiments'][0]
            speaker = aggregated_overlapping_tags['speaker'][0]

            clips.append(
                {"name": name_tag.value["value"],
                 "emotion": emotion,
                 "sentiment": sentiment,
                 "speaker": speaker,
                 "video_url": f"{youtube_url}?t={start_time:.0f}",
                 "start_time": int(start_time)
                 }
            )

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Sentiments", "Emotions"))
    c = dict(global_aggregated_tags["sentiments"].most_common(None))
    if c:
        fig.add_trace(go.Bar(x=list(c.keys()), y=list(c.values())), row=1, col=1)
    else:
        fig.add_annotation(text="No matching data found",
                           xref="paper", yref="paper", align="center",
                           showarrow=False, row=1, col=1)
        fig.update_xaxes(visible=False, row=1, col=1)
        fig.update_yaxes(visible=False, row=1, col=1)

    c = dict(global_aggregated_tags["emotions"].most_common(None))
    if c:
        fig.add_trace(go.Bar(x=list(c.keys()), y=list(c.values())), row=1, col=2)
    else:
        fig.add_annotation(text="No matching data found",
                           xref="paper", yref="paper", showarrow=False, row=1, col=2)
        fig.update_xaxes(visible=False, row=1, col=2)
        fig.update_yaxes(visible=False, row=1, col=2)

    fig.update_layout(showlegend=False)
    st.markdown("### Insights")
    st.plotly_chart(fig)

    st.markdown("### Clips")
    for clip in clips:
        st.markdown(f'#### {clip["name"]}')
        st.write(f"Emotion: {STYLED_EMOTIONS.get(clip['emotion'], clip['emotion'])}")
        st.write(f"Sentiment: {STYLED_SENTIMENTS.get(clip['sentiment'], clip['sentiment'])}")
        st.write(f"Speaker: {'Joe Rogan' if clip['speaker'] == 'spk_1' else 'Elon Musk'}")
        st.video(data=clip["video_url"], start_time=clip["start_time"])
