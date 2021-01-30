import random

from xeriff_ripoll.config import config

class LyricExtractor:

    def __init__(self, max_lines_per_paragraph: int=None):
        self.max_lines_per_paragraph = max_lines_per_paragraph or config.EXCERPT_MAX_LINES_PER_PARAGRAPH

    def execute(self, lyrics: str) -> str:
        lyric_paragraphs = lyrics.split("\n\n")

        candidate_paragraph = random.choice(lyric_paragraphs)
        paragraph_lines = candidate_paragraph.split("\n")

        if len(paragraph_lines) > self.max_lines_per_paragraph:
            paragraph_lines = self._shorten_paragraph(paragraph_lines)

        return "\n".join(map(lambda p: p.capitalize(), paragraph_lines))


    def _shorten_paragraph(self, paragraph: list) -> list:
        line_count = len(paragraph)
        start_index = random.randint(0, line_count - self.max_lines_per_paragraph)
        end_index = start_index + self.max_lines_per_paragraph

        return paragraph[start_index:end_index]

