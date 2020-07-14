import logging
from pathlib import Path

import click

from mypackage.demo.demo import Demo

logger = logging.getLogger(__name__)

DEFAULT_VERBOSITY = 0


def configure_logging(verbosity: int, quiet: int, json: bool = False) -> None:
    """Set the log level according to a level of verbosity and level of quietness"""

    # Base log level is WARNING, subtract the verbosity and add the quietness
    log_level = logging.WARNING - (verbosity * 10) + (quiet * 10)
    logger.debug(
        f"Setting log_level to {log_level} using q '{quiet}' and v '{verbosity}'"
    )

    # If JSON output is requested
    log_fmt: str = logging.BASIC_FORMAT

    if json:
        log_fmt = (
            '{"message": "%(message)s", "level": "%(levelname)s", "name": "%(name)s", '
            '"asctime": "%(asctime)s"}'
        )

    logging.basicConfig(format=log_fmt, level=log_level)


#########
# Menus #
#########

logo: str = r"""
 ______        ______            _                      
|  ___ \      (_____ \          | |                     
| | _ | |_   _ _____) )___  ____| |  _ ____  ____  ____ 
| || || | | | |  ____/ _  |/ ___) | / ) _  |/ _  |/ _  )
| || || | |_| | |   ( ( | ( (___| |< ( ( | ( ( | ( (/ / 
|_||_||_|\__  |_|    \_||_|\____)_| \_)_||_|\_|| |\____)
        (____/                             (_____|      
"""


@click.group()
@click.version_option(
    prog_name="MyPackage", message=f"{logo}\n%(prog)s, version %(version)s"
)
def main() -> None:
    """
    Welcome to the MyPackage CLI
    """
    pass


@main.group()
def demo() -> None:
    """
    Commands related to the demo.
    """
    pass


@demo.command()
@click.argument("input-dir", nargs=1, required=True, type=click.Path())
@click.argument("output-dir", nargs=1, required=False, type=click.Path())
@click.option(
    "-v", count=True, help="Increase logging verbosity", default=DEFAULT_VERBOSITY,
)
@click.option("-q", count=True, help="Decrease logging verbosity", default=0)
@click.option(
    "-o-json",
    is_flag=True,
    type=bool,
    help="Format the output logs as JSON",
    default=False,
)
def test(input_dir: str, output_dir: str, v: int, q: int, o_json: bool) -> None:
    configure_logging(v, q, o_json)

    try:
        Demo(input_dir, output_dir)
        exit(0)
    except Exception as error:
        logger.critical(error)
        exit(1)


if __name__ == "__main__":
    main()
