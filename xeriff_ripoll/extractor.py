import random

from xeriff_ripoll.config import config

class LyricExtractor:

    def __init__(self, max_length: int=None):
        self.max_length = max_length or config.EXCERPT_MAX_LENGTH

    def execute(self, lyrics: str) -> str:
        lyric_paragraphs = lyrics.split("\n\n")

        candidate_paragraph = random.choice(lyric_paragraphs)
        if len(candidate_paragraph) <= self.max_length:
            return candidate_paragraph

        return self._shorten_paragraph(candidate_paragraph)

    def _shorten_paragraph(self, paragraph: str) -> str:
        lines = paragraph.split("\n")

        must_reverse = random.randint(0, 1)
        if must_reverse:
            lines = reversed(lines)

        shortened_paragraph = []
        shortened_paragraph_length = 0
        for line in lines:
            line_length = len(line)
            if shortened_paragraph_length + line_length > self.max_length:
                break

            shortened_paragraph.append(line)
            shortened_paragraph_length += line_length

        if must_reverse:
            shortened_paragraph = reversed(shortened_paragraph)

        return "\n".join(shortened_paragraph)

