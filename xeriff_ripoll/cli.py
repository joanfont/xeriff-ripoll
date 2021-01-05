import click

from xeriff_ripoll import actions


@click.group()
def cli():
    pass


@cli.command()
def fetch():
    action = actions.FetchAndSaveLyrics()
    action.execute()


@cli.command()
@click.argument('song_id')
def get(song_id):
    action = actions.GetSongById()
    song = action.execute(song_id)
    print_song(song)


@cli.command()
def random():
    action = actions.GetRandomSongWithExcerpt()
    song = action.execute()
    print_song(song)


@cli.command()
def excerpt():
    action = actions.GetRandomSongWithExcerpt()
    song = action.execute()
    print_song(song, with_lyrics=False)
    print()
    print(song.excerpt)

@cli.command()
def tweet():
    action = actions.TweetRandomExcerpt()
    action.execute()


def print_song(song, with_lyrics=True):
    print(f'Title: {song.title}')
    print(f'URL: {song.url}')

    if with_lyrics:
        print()
        print(song.lyrics)