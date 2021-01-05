from bs4 import BeautifulSoup, Tag
import httpx

from xeriff_ripoll.entities import SongBuilder, Song
from xeriff_ripoll.utils import get_querystring_from_url



class LyricParser:
    BASE_HOST = 'http://produccionsblau.com'
    SONGS_URL = '/ossifar/index.php?aixo-es=las-cansiones'

    def __init__(self, http: httpx._client.BaseClient=None, song_builder: SongBuilder=None):
        self.http = http or httpx.Client()
        self.song_builder = song_builder or SongBuilder()

    def list_songs(self) -> list[Song]:
        url = '{base_host}{songs_url}'.format(base_host=self.BASE_HOST, songs_url=self.SONGS_URL)
        response = self.http.get(url)
        soup = self._get_soup(response.text)
        songs_container = soup.find('div', id='cansiones')
        song_items = songs_container.find_all('a')
        return list(map(self._build_song, song_items))

    def get_lyrics_by_song(self, song: Song) -> Song:
        response = self.http.get(song.url)
        soup = self._get_soup(response.text)
        lyrics_container = soup.find('div', class_='Section1')
        first_paragraph = lyrics_container.find('p')
        first_paragraph.decompose()

        return self.song_builder \
            .with_id(song.id) \
            .with_title(song.title) \
            .with_url(song.url) \
            .with_lyrics(lyrics_container.text) \
            .build()

    def _build_song(self, song_item: Tag) -> Song:
        song_title = song_item.text
        song_url = '{base_host}{song_url}'.format(base_host=self.BASE_HOST, song_url=song_item['href'])

        query_string = get_querystring_from_url(song_url)
        song_id = query_string.get('cansion')

        return self.song_builder \
            .with_id(int(song_id[0])) \
            .with_title(song_title) \
            .with_url(song_url) \
            .build()

    def _get_soup(self, html) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')


