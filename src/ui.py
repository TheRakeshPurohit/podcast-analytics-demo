"""Collection of helper functions to draw the ui with Streamlit."""
from time import perf_counter
from typing import List, Union

import plotly.graph_objects as go
import streamlit as st
from steamship import Tag

from src.data import load_guest_tags, load_topics, get_entity_tags_by_topic, fetch_youtube_url
from src.utils import get_steamship_client

STYLED_EMOTIONS = {"happiness": "Happy 😁", "anger": "Angry 😡", "unknown": "Not sure 🤧"}

STYLED_SENTIMENTS = {
    "POS": "Positive 👍",
    "POSITIVE": "Positive 👍",
    "NEG": "Negative 👎",
    "NEGATIVE": "Negative 👎",
    "NEUTRAL": "Neutral 🇨🇭",
}

INTERESTING_SENTIMENTS = {
    "NEGATIVE": {"title": "Negative", "color": "#FF4E4E"},
    "NEUTRAL": {"title": "Positive", "color": "#CECECE"},
    "POSITIVE": {"title": "Neutral", "color": "#55D078"},
}

STYLED_TAGS = {"emotions": STYLED_EMOTIONS, "sentiments": STYLED_SENTIMENTS}


def select_guest():
    """Select one of the guests that appeared on the podcast."""
    guest_to_file_ids = load_guest_tags()
    guest, file_ids = st.selectbox("Guest", options=guest_to_file_ids.items(), format_func=lambda x: x[0])
    if not guest:
        st.markdown("Please select a guest.")
    else:
        return guest, list(file_ids)


def select_topic():
    """Select one of the topics mentioned on the podcasts."""
    return st.selectbox("Topic", options=load_topics())


def list_clips_for_topics(
        selected_topic: str,
        selected_speaker: str = None,
) -> None:
    """List the Youtube clips mentioning one or more topics."""
    entity_tags = get_entity_tags_by_topic(selected_topic, selected_speaker)
    unique_entity_tags = dict(
        sorted(
            {
                tag.start_idx: tag
                for tag in entity_tags
            }.items(),
            key=lambda x: x,
        )
    ).values()

    placeholder = st.empty()

    st.markdown("## Clips")

    sentiments = []

    t0 = perf_counter()
    for ix, entity_tag in enumerate(unique_entity_tags):
        sentiment_tags = Tag.query(get_steamship_client(),
                                   tag_filter_query=f'blocktag and kind "sentiment" and overlaps {{tag_id "{entity_tag.id}"}}').data.tags
        sentiment = sentiment_tags[0].name
        sentiments.append(sentiment_tags[0].name)

        speaker_tags = Tag.query(get_steamship_client(),
                                 tag_filter_query=f'blocktag and kind "speaker" and overlaps {{tag_id "{entity_tag.id}"}}').data.tags
        speaker = speaker_tags[0].name
        start_time = float(entity_tag.value["start_time"] // 1_000)
        youtube_url = fetch_youtube_url(entity_tag.file_id)
        video_url = f"{youtube_url}?t={start_time:.0f}"

        st.markdown(f"#### Clip {ix + 1}")
        st.write(f"Sentiment: {STYLED_SENTIMENTS.get(sentiment, sentiment)}")
        st.write(f"Speaker: {speaker}")
        st.video(data=video_url, start_time=int(start_time))
        st.write(video_url)
    print("timing", perf_counter() - t0)
    counts = [
        sentiments.count(sentiment) / len(sentiments) * 100 for sentiment in INTERESTING_SENTIMENTS
    ]
    with placeholder.container():
        print("plotting stats")
        plot_sentiment_stats(counts, list(INTERESTING_SENTIMENTS),
                             [props["color"] for props in INTERESTING_SENTIMENTS.values()])


def plot_sentiment_stats(x: List[Union[int, float]], y: List[str], colors: List[str]) -> None:
    """Display the sentiment distribution on a horizontal bar plot."""
    fig = go.Figure()

    for ix, xd in enumerate(x):
        fig.add_trace(
            go.Bar(
                x=[xd],
                y=[0],
                orientation="h",
                marker=dict(
                    color=colors[ix],
                ),
                hovertemplate="<br>".join(
                    [
                        f"Label: {y[ix]}",
                        "Relative Frequency: %{x:.2f}%",
                    ]
                ),
            )
        )

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode="stack",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        autosize=False,
        height=50,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    annotations = []

    space = 0
    for xd, yd in zip(x, y):
        # labeling the rest of percentages for each bar (x_axis)
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=space + (xd / 2),
                y=0,
                text=f"{yd} ({xd:.2f}%)",
                font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                showarrow=False,
            )
        )
        space += xd

    fig.update_layout(annotations=annotations)

    st.plotly_chart(fig)


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
