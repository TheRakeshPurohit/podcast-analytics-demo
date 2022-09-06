"""Collection of helper functions to draw the ui with Streamlit."""
from collections import Counter, defaultdict
from typing import List, Union

import streamlit as st
from steamship import Tag

from src.data import load_file, load_guests, load_topics

STYLED_EMOTIONS = {"happiness": "Happy 😁", "anger": "Angry 😡", "unknown": "Not sure 🤧"}

STYLED_SENTIMENTS = {
    "POS": "Positive 👍",
    "POSITIVE": "Positive 👍",
    "NEG": "Negative 👎",
    "NEGATIVE": "Negative 👎",
    "NEUTRAL": "Neutral 🇨🇭",
}

STYLED_TAGS = {"emotions": STYLED_EMOTIONS, "sentiments": STYLED_SENTIMENTS}


def select_guest():
    """Select one of the guests that appeared on the podcast."""
    guest_tags = load_guests()

    guest_tag = st.selectbox("Guest", options=guest_tags, format_func=lambda x: x.name)
    if not guest_tag:
        st.markdown("Please select a guest.")
    else:
        file = load_file(guest_tag.file_id)
        tags = file.blocks[0].tags
        youtube_url = [tag.name for tag in file.tags if tag.kind == "youtube_url"][0]
        return guest_tag.name, youtube_url, tags


def select_topic():
    """Select one of the topics mentioned on the podcasts."""
    topics = load_topics()

    topic = st.selectbox("Topic", options=topics, format_func=lambda x: x.title())

    file_ids = topics[topic]
    if not file_ids:
        st.markdown("Please select a topic.")
    else:
        return topic, [load_file(file_id) for file_id in file_ids]


def list_clips_for_topics(
        youtube_url: str,
        selected_topics: Union[List[str], List[Tag]],
        tags: List[Tag],
        speaker: str = None,
) -> None:
    """List the Youtube clips mentioning one or more topics."""
    global_aggregated_tags = defaultdict(Counter)
    if (
            isinstance(selected_topics, list)
            and len(selected_topics) > 0
            and isinstance(selected_topics[0], str)
    ):
        selected_topics = dict(
            sorted(
                {
                    tag.start_idx: tag
                    for tag in tags
                    if tag.kind == "entities"
                       and (
                               tag.value["value"].lower() in selected_topics
                               or tag.name.lower() in selected_topics
                       )
                }.items(),
                key=lambda x: x,
            )
        ).values()
    clips = []
    for name_tag in selected_topics:
        aggregated_overlapping_tags = defaultdict(list)

        for tag in [
            tag
            for tag in tags
            if tag.kind not in {"entities", "article-topics", "timestamp"}
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

        start_time = float(name_tag.start_idx // 1_000)

        emotion = aggregated_overlapping_tags["emotions"][0]
        sentiment = aggregated_overlapping_tags["sentiments"][0]
        speaker = speaker or aggregated_overlapping_tags["speaker"][0]

        clips.append(
            {
                "name": name_tag.value["value"],
                "emotion": emotion,
                "sentiment": sentiment,
                "speaker": speaker,
                "video_url": f"{youtube_url}?t={start_time:.0f}",
                "start_time": int(start_time),
            }
        )

    # fig = make_subplots(rows=1, cols=2, subplot_titles=("Sentiments", "Emotions"))
    # c = dict(global_aggregated_tags["sentiments"].most_common(None))
    # if c:
    #     fig.add_trace(go.Bar(x=list(c.keys()), y=list(c.values())), row=1, col=1)
    # else:
    #     fig.add_annotation(
    #         text="No matching data found",
    #         xref="paper",
    #         yref="paper",
    #         align="center",
    #         showarrow=False,
    #         row=1,
    #         col=1,
    #     )
    #     fig.update_xaxes(visible=False, row=1, col=1)
    #     fig.update_yaxes(visible=False, row=1, col=1)
    #
    # c = dict(global_aggregated_tags["emotions"].most_common(None))
    # if c:
    #     fig.add_trace(go.Bar(x=list(c.keys()), y=list(c.values())), row=1, col=2)
    # else:
    #     fig.add_annotation(
    #         text="No matching data found", xref="paper", yref="paper", showarrow=False, row=1, col=2
    #     )
    #     fig.update_xaxes(visible=False, row=1, col=2)
    #     fig.update_yaxes(visible=False, row=1, col=2)
    #
    # fig.update_layout(showlegend=False)
    # st.markdown("### Insights")
    # st.plotly_chart(fig)

    st.markdown("## Clips")
    for ix, clip in enumerate(clips):
        st.markdown(f"#### Clip {ix + 1}")
        # st.write(f"Emotion: {STYLED_EMOTIONS.get(clip['emotion'], clip['emotion'])}")
        # st.write(f"Sentiment: {STYLED_SENTIMENTS.get(clip['sentiment'], clip['sentiment'])}")
        # st.write(f"Speaker: {'Joe Rogan' if clip['speaker'] == 'spk_1' else 'Elon Musk'}")
        st.video(data=clip["video_url"], start_time=clip["start_time"])
        st.write(clip["video_url"])


def footer():
    """Show the Made with <3 footer."""
    hide_streamlit_style = """
            <style>

footer {
visibility: hidden;
}
footer:after {
content:'Made with ❤️ by Steamship';
color: rgba(0,0,0,1);
visibility: visible;
display: block;
position: relative;
padding: 5px;
top: 2px;
}
</style>

"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
