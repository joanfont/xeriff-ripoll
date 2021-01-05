from dataclasses import dataclass

from xeriff_ripoll.config import config

import tweepy

@dataclass
class Credentials:
    api_key: str
    api_key_secret: str
    access_token: str
    access_token_secret: str


def make_default_credentials():
    return Credentials(
        api_key=config.TWITTER_API_KEY,
        api_key_secret=config.TWITTER_API_KEY_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
    )


class Client:

    def __init__(self, credentials: Credentials=None):
        self.credentials = credentials or make_default_credentials()
        auth = tweepy.OAuthHandler( self.credentials.api_key,  self.credentials.api_key_secret)
        auth.set_access_token( self.credentials.access_token,  self.credentials.access_token_secret)
        self.api = tweepy.API(auth)

    def post(self, message):
        self.api.update_status(message)
