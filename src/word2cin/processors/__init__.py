
import logging
from typing import List
from word2cin.config_loader import DataSourceBase, DataSourceType
from word2cin.processors.process_chhoe_taigi import process_chhoe_taigi_data
from word2cin.processors.process_gsheet import process_google_sheet_data

logger = logging.getLogger(__name__)


def process_data_sources(data_sources: List[DataSourceBase]):
    cin_data_dict = {}
    for data_source in data_sources:
        if data_source.type == DataSourceType.CHHOE_TAIGI_DATABASE:
            cin_data = process_chhoe_taigi_data(data_source)
        elif data_source.type == DataSourceType.GOOGLE_SHEET:
            cin_data = process_google_sheet_data(data_source)
        else:
            raise ValueError(str(data_source.type) + " is unknown.")
        cin_data_dict[data_source.name] = cin_data
    return cin_data_dict
