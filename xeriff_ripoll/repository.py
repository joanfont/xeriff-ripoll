from abc import ABCMeta, abstractmethod
import glob
import json
import os
import random

from xeriff_ripoll.filesystem import Filesystem
from xeriff_ripoll.entities import SongBuilder, Song


class LyricRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, song) -> Song:
        pass

    @abstractmethod
    def get_all(self) -> list[Song]:
        pass

    @abstractmethod
    def get_by_song_id(self, song_id) -> Song:
        pass

    @abstractmethod
    def get_random_song(self) -> Song:
        pass

class FilesystemLyricRepository(LyricRepository):

    def __init__(self, base_path: str, filesystem: Filesystem=None, song_builder: SongBuilder=None):
        self.base_path = base_path
        self.filesystem = filesystem or Filesystem()
        self.song_builder = song_builder or SongBuilder()

    def save(self, song) -> Song:
        data = {
            'id' : song.id,
            'title': song.title,
            'url': song.url,
            'lyrics': song.lyrics,
        }

        file_name = self._get_file_name(song.id)
        self.filesystem.write(file_name, 'w', json.dumps(data, indent=4))
        return song

    def get_all(self) -> list[Song]:
        all_songs = self._get_all_songs()
        return list(map(self._get_song_by_file, all_songs))

    def get_by_song_id(self, song_id) -> Song:
        file_name = self._get_file_name(song_id)
        return self._get_song_by_file(file_name)

    def get_random_song(self) -> Song:
        random_song_file = self._get_random_song_file()
        return self._get_song_by_file(random_song_file)

    def _get_all_songs(self) -> list[str]:
        all_songs_path = self._get_file_name('*')
        return glob.glob(all_songs_path)

    def _get_random_song_file(self) -> str:
        all_songs = self._get_all_songs()
        return random.choice(all_songs)

    def _get_song_by_file(self, file_path) -> Song:
        song = json.loads(self.filesystem.read(file_path, 'r'))

        return self.song_builder \
            .with_id(song['id']) \
            .with_title(song['title']) \
            .with_url(song['url']) \
            .with_lyrics(song['lyrics']) \
            .build()


    def _get_file_name(self, song_id) -> str:
        return os.path.join(
            self.base_path,
            f'{song_id}.json'
        )
