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


"""
- The project should be stored in GitHub and you should only commit relevant files to the repo.
V Save the output in a **client_data** directory in the root directory of the project.
- Add a **README** file explaining on a high level what the application does.
V Application should receive three arguments, the paths to each of the dataset files and also the countries to filter as the client wants to reuse the code for other countries.
V Use **logging**.
- Create generic functions for filtering data and renaming.
Recommendation: Use the following package for Spark tests - https://github.com/MrPowers/chispa
- If possible, have different branches for different tasks that once completed are merged to the main branch. Follow the GitHub flow - https://guides.github.com/introduction/flow/.
- **Bonus** - If possible it should have an automated build pipeline using  https://www.travis-ci.com/ for instance.
V **Bonus** - If possible log to a file with a rotating policy.
- **Bonus** - Code should be able to be packaged into a source distribution file.
- **Bonus** - Requirements file should exist.
- **Bonus** - Document the code with docstrings as much as possible using the reStructuredText (reST) format.
"""
