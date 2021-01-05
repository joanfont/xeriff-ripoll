from xeriff_ripoll.config import config
from xeriff_ripoll.entities import SongBuilder, Song
from xeriff_ripoll.extractor import LyricExtractor
from xeriff_ripoll.parser import LyricParser
from xeriff_ripoll.processors import LyricCleaner
from xeriff_ripoll.repository import FilesystemLyricRepository, LyricRepository
from xeriff_ripoll.twitter import Client as TwitterClient


class FetchAndSaveLyrics:

    def __init__(self,
        lyric_parser: LyricParser=None,
        lyric_cleaner: LyricCleaner=None,
        lyric_repository: LyricRepository=None
    ):
        self.lyric_parser = lyric_parser or LyricParser()
        self.lyric_cleaner = lyric_cleaner or LyricCleaner()
        self.lyric_repository = lyric_repository or FilesystemLyricRepository(config.LYRICS_PATH)

    def execute(self):
        songs = self.lyric_parser.list_songs()
        for song in songs:
            song_with_lyrics = self.lyric_parser.get_lyrics_by_song(song)
            song_with_lyrics.lyrics = self.lyric_cleaner.execute(song_with_lyrics.lyrics)
            self.lyric_repository.save(song_with_lyrics)


class GetSongById:

    def __init__(self, lyric_repository: LyricRepository=None):
        self.lyric_repository = lyric_repository or FilesystemLyricRepository(config.LYRICS_PATH)

    def execute(self, song_id: int) -> Song:
        return self.lyric_repository.get_by_song_id(song_id)


class GetRandomSong:

    def __init__(self, lyric_repository: LyricRepository=None):
        self.lyric_repository = lyric_repository or FilesystemLyricRepository(config.LYRICS_PATH)

    def execute(self) -> Song:
        return self.lyric_repository.get_random_song()


class GetRandomSongWithExcerpt:

    def __init__(
        self,
        get_random_song: GetRandomSong=None,
        lyric_extractor: LyricExtractor=None,
        song_builder: SongBuilder=None
    ):
        self.get_random_song = get_random_song or GetRandomSong()
        self.lyric_extractor = lyric_extractor or LyricExtractor()
        self.song_builder = song_builder or SongBuilder()

    def execute(self) -> Song:
        random_song = self.get_random_song.execute()
        excerpt = self.lyric_extractor.execute(random_song.lyrics)
        return self.song_builder \
            .with_id(random_song.id) \
            .with_title(random_song.title) \
            .with_url(random_song.url) \
            .with_lyrics(random_song.lyrics) \
            .with_excerpt(excerpt) \
            .build()


class TweetRandomExcerpt:

    def __init__(
            self,
            get_random_song_with_excerpt: GetRandomSongWithExcerpt=None,
            twitter_client: TwitterClient=None
    ):
        self.get_random_song_with_excerpt = get_random_song_with_excerpt or GetRandomSongWithExcerpt()
        self.twitter_client = twitter_client or TwitterClient()

    def execute(self):
        random_song_with_excerpt = self.get_random_song_with_excerpt.execute()
        self.twitter_client.post(random_song_with_excerpt.excerpt)