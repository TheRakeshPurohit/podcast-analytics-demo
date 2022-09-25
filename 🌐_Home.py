"""Main UI for the podcast analytics app."""
from pathlib import Path

import streamlit as st

from src.auth import authenticate, TYPEFORM_FORM
from src.ui import footer

st.set_page_config(
    page_title="The Joe Rogan Index  📒",
    page_icon=Path("data/logo.png").open("rb").read(),
    layout="centered",
)
footer()

st.title("The Joe Rogan Index 📒")

redirect_uri = st.secrets["redirect_uri"]
st.markdown(f"### 💡 Topics \n "
            "Explore what Joe Rogan and his guests have to say about topics of your interest. "
            " \n "
            f"### 🤓 TLDR \n "
            "Catch up with Joe Rogan by reading summaries of his podcasts. \n"
            "## How I built this \n"
            "* Transcription: [AssemblyAI](https://www.assemblyai.com/)\n"
            "* Language AI: [OneAI](https://www.oneai.com/), [AssemblyAI](https://www.assemblyai.com/), and [Huggingface](https://huggingface.co/)\n"
            "* Database: [Steamship](https://steamship.com) \n"
            "* Deployment: [Steamship](https://steamship.com) \n"
            "* UI: [Streamlit](https://streamlit.io/) \n"
            "## Why I built this \n"
            f"🤣 [Read my blog post]"
            f"(https://medium.com/steamship/im-consuming-5000-hours-of-joe-rogan-with-the-help-of-ai-9cb7cc7a4985). \n "
            "## Index your own podcasts \n"
            f"I bundled all the code in a re-usable Steamship package. [Click here]({TYPEFORM_FORM}) you're interested in indexing your own podcasts. ")

authenticate()

st.markdown("## Getting started \n"
            "Click one of the links in the sidebar (👈) to get started.")

footer()
