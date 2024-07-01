import logging
from pathlib import Path
import sys

from word2cin.config_loader import create_config_from_yaml
from word2cin.processors import process_data_sources

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def get_yaml_path():
    import word2cin
    return Path(Path(word2cin.__file__).parent, "config.yaml")


def main():
    cfg = create_config_from_yaml(get_yaml_path())
    logger.info(cfg)
    cin_data = process_data_sources(cfg.data_sources)
    # save_cin(cfg, cin_data)


if __name__ == "__main__":
    main()