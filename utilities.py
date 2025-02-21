from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import datetime
import streamlit as st


def get_api_headers():
    client_id = 'cd2d3ad1-94e4-4a2f-8bac-40c9db83e1f2'
    client_secret = 'oQuxOWArbMnmGeMrkxQnTCmvx6XykM6O'

    # Create a session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # Get token for the session
    token_url = 'https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token'
    token = oauth.fetch_token(token_url=token_url, client_secret=client_secret, include_client_id=True)

    # API endpoint for Sentinel Hub's Process API (POST request)
    api_url = 'https://creodias.sentinel-hub.com/api/v1/process'

    # Headers for the request
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
        'Content-Type': 'application/json'}

    return headers

import datetime

def get_dates():
    # Get the current date and time in UTC
    today = datetime.datetime.utcnow()
    # Subtract 48 hours (2 days) from the current date and time
    from_time = today - datetime.timedelta(hours=48)
    # Format the dates as strings in the desired format
    current_time= today.strftime("%Y-%m-%dT%H:%M:%SZ")
    past_time = from_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return past_time, current_time

past_time, current_time = get_dates()
