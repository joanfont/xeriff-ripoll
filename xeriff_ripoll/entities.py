from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Song:
    id: int
    title: str
    url: str
    lyrics: str = None
    excerpt: str = None


class SongBuilder:

    def __init__(self):
        self.params = {}

    def with_id(self, id_: int) -> SongBuilder:
        self.params['id'] = id_
        return self

    def with_title(self, title: str) -> SongBuilder:
        self.params['title'] = title
        return self

    def with_url(self, url: str) -> SongBuilder:
        self.params['url'] = url
        return self

    def with_lyrics(self, lyrics: str) -> SongBuilder:
        self.params['lyrics'] = lyrics
        return self

    def with_excerpt(self, excerpt: str) -> SongBuilder:
        self.params['excerpt'] = excerpt
        return self

    def build(self) -> Song:
        return Song(**self.params)
