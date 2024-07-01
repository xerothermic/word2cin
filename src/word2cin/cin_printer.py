import logging
import os
from word2cin.cin_entry import CinEntry
from word2cin.config_loader import CinPrinterConfig
from word2cin.processors.process_chhoe_taigi import dedup_cin_list

logger = logging.getLogger(__name__)


def print_header(ename, cname, selkey, fp):
    print("%gen_inp", file=fp)
    print(f"%ename {ename}", file=fp)
    print(f"%cname {cname}", file=fp)
    print("%encoding UTF-8", file=fp)
    print(f"%selkey {selkey}", file=fp)
    print_keyname(fp)
    print("%chardef begin", file=fp)


def print_keyname(fp):
    skip_list = "qwdfzxyv"
    print("%keyname begin", file=fp)
    for i in range(1, 10):
        print(f"{i} {i}", file=fp)

    for c in range(26):
        ch = chr(ord('a') + c)
        if ch in skip_list:
            continue
        print(f"{ch} {ch}", file=fp)
    print("%keyname end", file=fp)


def print_cin_entries(
        data_sources: list[str], cin_data: dict[str, CinEntry], fp, include_source):
    filtered_cin_data = [cin_entry for ds_name, cin_entries in cin_data.items(
    ) if ds_name in data_sources for cin_entry in cin_entries]
    filtered_cin_data = dedup_cin_list(filtered_cin_data)
    filtered_cin_data.sort(key=lambda c: c.weight)
    for c in filtered_cin_data:
        if include_source:
            print(f"{c.key} {c.value};{c.src_name};{c.parse_method}", file=fp)
        else:
            print(f"{c.key} {c.value}", file=fp)


def print_footer(fp):
    print("%chardef end", file=fp)


def create_out_dir_if_not_existed(out_dir: str):
    if not os.path.exists(out_dir):
        logger.info(f"{out_dir=} does not exist, creating it...")
        os.mkdir(out_dir)


def save_cin(cfgs: list[CinPrinterConfig], cin_data: list[CinEntry]) -> None:
    for cfg in cfgs:
        create_out_dir_if_not_existed(cfg.out_dir)
        out_path = os.path.join(cfg.out_dir, cfg.out_filename)
        logger.info(f"{cfg.name} {out_path=}")
        with open(out_path, "w") as fp:
            print_header(cfg.ename, cfg.cname, cfg.selkey, fp)
            print_cin_entries(cfg.data_sources, cin_data, fp, cfg.include_source)
            print_footer(fp)
