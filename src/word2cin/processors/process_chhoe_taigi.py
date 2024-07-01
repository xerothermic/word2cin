from collections import defaultdict
import logging
from typing import List

import pandas as pd

from word2cin.cin_entry import CinEntry
from word2cin.config_loader import DataSource

logger = logging.getLogger(__name__)


def load_chhoe_taigi_dataframe(path: str):
    df = pd.read_csv(path)
    return df


def dedup_cin_list(cin_list: list[CinEntry]) -> list[CinEntry]:
    cin_map: dict[(str, str), CinEntry] = {}
    for e in cin_list:
        key = (e.key, e.value)
        exist = cin_map.get(key)
        if exist:
            e <<= exist
        cin_map[key] = e
    return list(cin_map.values())


def process_chhoe_taigi_data(data_source: DataSource):
    cin_list = []
    taigi_df = load_chhoe_taigi_dataframe(data_source.path)
    # logger.debug(taigi_df.head(5).to_string(line_width=150))
    for parse_method_cls in data_source.parse_methods:
        cin_data = parse_method_cls().parse(data_source.name, taigi_df)
        logger.debug(cin_data)
        cin_list.extend(cin_data)
    logger.info("cin_list len before dedup:" + str(len(cin_list)))
    cin_list = dedup_cin_list(cin_list)
    logger.info("cin_list len after dedup:" + str(len(cin_list)))
    return cin_list
