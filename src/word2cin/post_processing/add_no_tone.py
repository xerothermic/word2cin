from copy import deepcopy
import logging
from word2cin.cin_entry import CinEntry
from word2cin.post_processing.post_processing_base import PostProcessingBase

logger = logging.getLogger(__name__)


class AddNoTone(PostProcessingBase):
    def process(self, cin_data: list[CinEntry]) -> list[CinEntry]:
        NO_DIGIT_MAP = {ord(str(d)): None for d in (2, 3, 4, 5, 7, 8)}
        new_cin_data = []
        for c in cin_data:
            no_digit_key = c.key.translate(NO_DIGIT_MAP)
            if no_digit_key != "" and no_digit_key != c.key:
                new_c = deepcopy(c)
                new_c.key = no_digit_key
                new_cin_data.append(
                    new_c
                )
            new_cin_data.append(c)
        return new_cin_data
