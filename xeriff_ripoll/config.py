import decouple


class Config:

    @property
    def LYRICS_PATH(self) -> str:
        return decouple.config('LYRICS_PATH')

    @property
    def EXCERPT_MAX_LENGTH(self) -> int:
        return decouple.config('EXCERPT_MAX_LENGTH', cast=int, default=280)

    @property
    def TWITTER_API_KEY(self) -> str:
        return decouple.config('TWITTER_API_KEY')

    @property
    def TWITTER_API_KEY_SECRET(self) -> str:
        return decouple.config('TWITTER_API_KEY_SECRET')

    @property
    def TWITTER_ACCESS_TOKEN(self) -> str:
        return decouple.config('TWITTER_ACCESS_TOKEN')

    @property
    def TWITTER_ACCESS_TOKEN_SECRET(self) -> str:
        return decouple.config('TWITTER_ACCESS_TOKEN_SECRET')


config = Config()