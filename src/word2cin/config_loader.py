from dataclasses import dataclass
from enum import Enum
import logging
import yaml

from word2cin.parsers import PARSE_METHODS
from word2cin.parsers.parse_method_base import ParseMethodBase
from word2cin.post_processing import POST_PROCESSING_OPTIONS
from word2cin.post_processing.post_processing_base import PostProcessingBase

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    UNKNOWN = 0
    CHHOE_TAIGI_DATABASE = 1
    GOOGLE_SHEET = 2


@dataclass
class DataSource:
    name: str
    type: DataSourceType
    path: str
    parse_methods: list[ParseMethodBase]
    post_processing: list[PostProcessingBase]


@dataclass
class CinPrinterConfig:
    name: str
    data_sources: list[DataSource]
    ename: str
    cname: str
    selkey: str
    out_filename: str
    out_dir: str
    # include data source to chardef block. Mainly for debugging
    include_source: bool = False


@dataclass
class Config:
    data_sources: list[DataSource]
    cin_printer_cfgs: list[CinPrinterConfig]


def load_yaml_config(path) -> dict:
    with open(path, encoding="utf-8") as f:
        try:
            res = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(e)
            raise e
    return res


def get_parse_methods(data_source_dict) -> list[ParseMethodBase]:
    parse_methods = []
    if "parseMethods" not in data_source_dict:
        raise ValueError(" should include parseMethods")
    for parse_method_name in data_source_dict["parseMethods"]:
        if parse_method_name not in PARSE_METHODS or PARSE_METHODS[parse_method_name] is None:
            logger.warning(
                f"{parse_method_name} does not have an implementation yet.")
            continue
        parse_methods.append(PARSE_METHODS[parse_method_name])
    return parse_methods


def get_post_processing(data_source_dict) -> list[PostProcessingBase]:
    post_processing = []
    if "postProcessing" not in data_source_dict:
        return post_processing
    for post_processing_option in data_source_dict["postProcessing"]:
        if post_processing_option not in POST_PROCESSING_OPTIONS:
            logger.warning(
                f"{post_processing_option} does not have an implementation yet.")
            continue
        post_processing.append(POST_PROCESSING_OPTIONS[post_processing_option])
    return post_processing


def get_data_sources(yaml_dict) -> list[DataSource]:
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
            parse_methods,
            get_post_processing(ds_vals),
        )
        data_sources.append(ds)
    return data_sources


def get_cin_printer_cfgs(yaml_dict) -> list[CinPrinterConfig]:
    if "cinOutputs" not in yaml_dict:
        raise ValueError("yaml_dict should include cinOutputs")
    cin_output_yaml_cfgs = yaml_dict["cinOutputs"]
    cfgs = []
    for cfg_name, yaml_cfg in cin_output_yaml_cfgs.items():
        cfg = CinPrinterConfig(
            name=cfg_name,
            data_sources=yaml_cfg["dataSources"],
            ename=yaml_cfg["ename"],
            cname=yaml_cfg["cname"],
            selkey=yaml_cfg["selkey"],
            out_filename=yaml_cfg["out_filename"],
            out_dir=yaml_cfg.get("out_dir", "build/"),
            include_source=yaml_cfg.get("include_source", False),
        )
        logger.info(f"CinPrinterConfig:{cfg}")
        cfgs.append(cfg)
    return cfgs


def create_config(yaml_dict) -> Config:
    data_sources = get_data_sources(yaml_dict)
    cin_printer_cfgs = get_cin_printer_cfgs(yaml_dict)
    cfg = Config(data_sources, cin_printer_cfgs)
    return cfg


def create_config_from_yaml(path) -> Config:
    yaml_dict = load_yaml_config(path)
    cfg = create_config(yaml_dict)
    return cfg
