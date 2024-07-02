

from word2cin.cin_entry import CinEntry
from word2cin.post_processing.post_processing_base import PostProcessingBase


class ConvertKeyToLowerCase(PostProcessingBase):
    def process(self, cin_data: list[CinEntry]) -> list[CinEntry]:
        for c in cin_data:
            c.key = c.key.lower()
        assert not any([c.key[0] == "T" for c in cin_data])
        return cin_data

