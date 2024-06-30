import logging

import pandas as pd

from word2cin.config_loader import DataSource

logger = logging.getLogger(__name__)

def load_chhoe_taigi_dataframe(path: str):
    df = pd.read_csv(path)
    return df


def process_chhoe_taigi_data(data_source: DataSource):
    cin_data_list = []
    taigi_df = load_chhoe_taigi_dataframe(data_source.path)
    # logger.debug(taigi_df.head(5).to_string(line_width=150))
    for parse_method_cls in data_source.parse_methods:
        cin_map = parse_method_cls().parse(data_source.name, taigi_df)
        logger.debug(cin_map)
        cin_data_list.append(cin_map)
    return taigi_df