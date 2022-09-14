"""Collection of helper functions to draw the ui with Streamlit."""
from itertools import groupby

import streamlit as st

from src.data import load_guest_tags, load_topics, get_entity_tags_by_topic, fetch_youtube_url

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
    guest_to_file_ids = {k: {x.file_id for x in v} for k, v in
                         groupby(sorted(load_guest_tags(), key=lambda x: x.name), key=lambda x: x.name)}
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
    print("selected_topic", selected_topic)
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

    clips = []
    for entity_tag in unique_entity_tags:
        # aggregated_overlapping_tags = defaultdict(list)
        #
        # for tag in [
        #     tag
        #     for tag in tags
        #     if tag.kind not in {"entities", "article-topics", "timestamp"}
        #     if (tag.start_idx is None or tag.start_idx <= entity_tag.start_idx + len(entity_tag.name))
        #        and (tag.end_idx is None or tag.end_idx >= entity_tag.end_idx - len(entity_tag.name))
        # ]:
        #     aggregated_overlapping_tags[tag.kind].append(
        #         STYLED_TAGS.get(tag.kind, {}).get(tag.name, tag.name)
        #     )
        #
        # if "emotions" not in aggregated_overlapping_tags:
        #     aggregated_overlapping_tags["emotions"].append(STYLED_EMOTIONS["unknown"])
        #
        # if "sentiments" not in aggregated_overlapping_tags:
        #     aggregated_overlapping_tags["sentiments"].append(STYLED_SENTIMENTS["NEUTRAL"])
        #
        # if "speaker" not in aggregated_overlapping_tags:
        #     aggregated_overlapping_tags["speaker"].append("unkown")
        #
        # for tag_kind in ("emotions", "sentiments", "speaker"):
        #     global_aggregated_tags[tag_kind].update(aggregated_overlapping_tags[tag_kind])

        start_time = float(entity_tag.start_idx // 1_000)

        # emotion = aggregated_overlapping_tags["emotions"][0]
        # sentiment = aggregated_overlapping_tags["sentiments"][0]
        # speaker = speaker or aggregated_overlapping_tags["speaker"][0]
        youtube_url = fetch_youtube_url(entity_tag.file_id)

        clips.append(
            {
                "name": entity_tag.value["value"],
                # "emotion": emotion,
                # "sentiment": sentiment,
                "speaker": selected_speaker,
                "video_url": f"{youtube_url}?t={start_time:.0f}",
                "start_time": int(start_time),
            }
        )

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
