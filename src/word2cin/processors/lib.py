
import logging

from word2cin.cin_entry import CinEntry
from word2cin.post_processing.post_processing_base import PostProcessingBase


logger = logging.getLogger(__name__)


def parse_method_loop(data_source, taigi_df) -> list[CinEntry]:
    cin_list = []
    for parse_method_cls in data_source.parse_methods:
        cin_data = parse_method_cls().parse(data_source.name, taigi_df)
        is_empty = len(cin_data) == 0
        logger.log(
            logging.WARNING if is_empty else logging.INFO,
            f"{parse_method_cls.__name__} got {len(cin_data)} entries"
        )
        logger.debug(cin_data)
        cin_list.extend(cin_data)
    return cin_list


def post_processing_loop(post_processing: list[PostProcessingBase], cin_list):
    for post_processing_cls in post_processing:
        cin_list = post_processing_cls().process(cin_list)
    return cin_list


def dedup_cin_list(cin_list: list[CinEntry]) -> list[CinEntry]:
    cin_map: dict[(str, str), CinEntry] = {}
    for e in cin_list:
        key = (e.key, e.value)
        exist = cin_map.get(key)
        if exist:
            e <<= exist
        cin_map[key] = e
    return list(cin_map.values())
