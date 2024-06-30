from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import List
import yaml

from word2cin.parsers import PARSE_METHODS
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)

class DataSourceType(Enum):
    Unknown = 0
    ChhoeTaigiDatabase = 1
    GoogleSheet = 2

@dataclass
class DataSource:
    name: str
    type: DataSourceType
    path: str
    parse_methods: List[ParseMethodBase]

@dataclass
class CinPrinterConfig:
    name: str
    data_sources: List[DataSource]

@dataclass
class Config:
    data_sources: List[DataSource]
    cin_printer_cfgs: List[CinPrinterConfig]


def load_yaml_config(path) -> dict:
    with open(path, encoding="utf-8") as f:
        try:
            res = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(e)
            raise e
    return res

def get_parse_methods(data_source_dict) -> List[ParseMethodBase]:
    parse_methods = []
    if "parseMethods" not in data_source_dict:
        raise ValueError(" should include parseMethods")
    for parse_method_name in data_source_dict["parseMethods"]:
        if parse_method_name not in PARSE_METHODS:
            logger.warning(f"{parse_method_name} does not have an implementation yet.")
            continue
        parse_methods.append(PARSE_METHODS[parse_method_name])
    return parse_methods
    

def get_data_sources(yaml_dict) -> List[DataSource]:
    data_sources = []
    if "dataSources" not in yaml_dict:
        raise ValueError("yaml_dict should include dataSources")

    for ds_name, ds_vals in yaml_dict["dataSources"].items():
        try:
            parse_methods = get_parse_methods(ds_vals)
        except ValueError as e:
            raise ValueError(ds_name + str(e)) from e
        ds = DataSource(
            ds_name,
            DataSourceType[ds_vals["type"]],
            ds_vals["path"],
            parse_methods
        )
        data_sources.append(ds)
    return data_sources


def get_cin_printer_cfgs(yaml_dict) -> CinPrinterConfig:
    return CinPrinterConfig(name="dummy", data_sources=[])
    # raise NotImplementedError()


def create_config(yaml_dict) -> Config:
    data_sources = get_data_sources(yaml_dict)
    cin_printer_cfgs = get_cin_printer_cfgs(yaml_dict)
    cfg = Config(data_sources, cin_printer_cfgs)
    return cfg


def create_config_from_yaml(path) -> Config:
    yaml_dict = load_yaml_config(path)
    cfg = create_config(yaml_dict)
    return cfg