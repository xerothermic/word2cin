
import logging
from typing import List
from word2cin.config_loader import DataSource, DataSourceType
from word2cin.processors.process_chhoe_taigi import process_chhoe_taigi_data

logger = logging.getLogger(__name__)

def process_data_sources(data_sources: List[DataSource]):
    cin_data_dict = {}
    for data_source in data_sources:
        if data_source.type == DataSourceType.ChhoeTaigiDatabase:
            cin_data = process_chhoe_taigi_data(data_source)
        elif data_source.type == DataSourceType.GoogleSheet:
            raise NotImplementedError()
        cin_data_dict[data_source.name] = cin_data
    return cin_data_dict