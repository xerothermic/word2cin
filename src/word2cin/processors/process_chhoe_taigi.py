import logging

import pandas as pd

from word2cin.config_loader import DataSourceChhoeTaigiDb
from word2cin.processors.lib import dedup_cin_list, parse_method_loop, post_processing_loop

logger = logging.getLogger(__name__)


def load_chhoe_taigi_dataframe(path: str):
    df = pd.read_csv(path)
    return df


def process_chhoe_taigi_data(data_source: DataSourceChhoeTaigiDb):
    taigi_df = load_chhoe_taigi_dataframe(data_source.path)
    # logger.debug(taigi_df.head(5).to_string(line_width=150))
    cin_list = parse_method_loop(data_source, taigi_df)
    logger.info("cin_list len after parse_method_loop:" + str(len(cin_list)))
    cin_list = post_processing_loop(data_source.post_processing, cin_list)
    logger.info("cin_list len after post_processing_loop:" +
                str(len(cin_list)))
    cin_list = dedup_cin_list(cin_list)
    logger.info("cin_list len after dedup:" + str(len(cin_list)))
    return cin_list
