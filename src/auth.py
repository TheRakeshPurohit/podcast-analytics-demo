import asyncio
import base64
from pathlib import Path

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import GetAccessTokenError


def check_auth() -> None:
    client_id = st.secrets["google_oauth_client_id"]
    client_secret = st.secrets["google_oauth_client_secret"]
    redirect_uri = st.secrets["redirect_uri"]

    client = GoogleOAuth2(client_id, client_secret)

    authorization_url = asyncio.run(
        client.get_authorization_url(
            redirect_uri, scope=["email"]
        )
    )

    if "token" not in st.session_state:
        try:
            code = st.experimental_get_query_params()["code"]
            token = asyncio.run(client.get_access_token(code, redirect_uri))

        except (KeyError, GetAccessTokenError):
            show_login_prompt(authorization_url)
        else:
            if token.is_expired():
                show_login_prompt(authorization_url)
            else:
                st.session_state["token"] = token
                user_id, user_email = asyncio.run(client.get_id_email(token["access_token"]))

                st.session_state["user_id"] = user_id
                st.session_state["user_email"] = user_email
                st.sidebar.write(f'Welcome {st.session_state["user_email"]}')
    else:
        st.sidebar.write(f'Welcome {st.session_state["user_email"]}')


def show_login_prompt(authorization_url):
    st.sidebar.markdown("Please sign in to use our app:")

    image = Path("google_login_button.png")
    file_ = image.open("rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.sidebar.write(
        f"""<a target="_blank"
                                  href="{authorization_url}">
                                  <image src="data:image/gif;base64,{data_url}" width="200px">
                                  </a>""",
        unsafe_allow_html=True,
    )
    st.stop()
