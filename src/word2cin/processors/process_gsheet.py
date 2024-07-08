
import logging

import pandas as pd

from word2cin.config_loader import DataSourceGoogleSheet
from word2cin.processors.lib import dedup_cin_list, parse_method_loop, post_processing_loop


logger = logging.getLogger(__name__)


def load_google_sheet_dataframe(
        gsheet_key: str,
        sheet_name: str) -> pd.DataFrame:
    gsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheet_key}/export?/format=xlsx"
    # NOTE: explicit set below columns to str for pure digit values.
    taigi_df = pd.read_excel(gsheet_url, sheet_name, dtype={"KipInput": str, "KipUnicode": str, "HanLoTaibunKip": str})
    return taigi_df


def process_google_sheet_data(data_source: DataSourceGoogleSheet):
    taigi_df = load_google_sheet_dataframe(
        data_source.gsheet_key, data_source.sheet_name)
    logger.debug(taigi_df.head(5).to_string(line_width=150))
    cin_list = parse_method_loop(data_source, taigi_df)
    logger.info("cin_list len after parse_method_loop:" + str(len(cin_list)))
    cin_list = post_processing_loop(data_source.post_processing, cin_list)
    logger.info("cin_list len after post_processing_loop:" +
                str(len(cin_list)))
    cin_list = dedup_cin_list(cin_list)
    logger.info("cin_list len after dedup:" + str(len(cin_list)))
    return cin_list
