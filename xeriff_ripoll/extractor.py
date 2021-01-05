import random

class LyricExtractor:

    def execute(self, lyrics: str) -> str:
        lyric_paragraphs = lyrics.split("\n\n")
        return random.choice(lyric_paragraphs)

