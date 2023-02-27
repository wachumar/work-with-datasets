import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys

import pandas as pd

from processing import prepare_data


logging.basicConfig(
    handlers=[RotatingFileHandler("log_records.log", maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Prepare dataset from two tables",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-x", "--client-info-path", help="Client information source location"
    )
    parser.add_argument(
        "-y", "--client-financial-path", help="Client financial source location"
    )
    parser.add_argument("-c", "--countries", nargs="*", help="Country to filter")
    parser.add_argument(
        "-d",
        "--default",
        action="store_true",
        help="Use default params for paths and countries",
    )
    args = parser.parse_args()
    config = vars(args)

    prepare_data(config)


if __name__ == "__main__":
    main(sys.argv[1:])
