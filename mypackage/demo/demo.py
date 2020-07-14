import json
import logging
from os.path import sep
from pathlib import Path

logger = logging.getLogger(__name__)


class DemoInputFileDoesNotExistException(Exception):
    message: str

    def __init__(self, file_name: str):
        """Initialize the exception with the file_name of the missing file"""

        self.message = f"Input file '{file_name}' does not exist"


class DemoOutputFileDoesNotExistException(Exception):
    message: str

    def __init__(self, file_name: str):
        """Initialize the exception with the file_name of the missing file"""

        self.message = f"Output file '{file_name}' does not exist"


class Demo:
    """
    A class that represents a Demo.
    """

    input_path: Path
    output_path: Path

    def __init__(self, input_path: str, output_path: str = None) -> None:
        """
        Initialize a demo
        :param input_path: input file path
        :param output_path: output file path
        """
        self.input_path = Path(input_path).absolute()
        if not self.input_path.is_file():
            logger.error(f"Input file '{input_path}' does not exist")
            raise DemoInputFileDoesNotExistException(input_path)

        if output_path is None:
            input_dir: Path = self.input_path.parents[0]
            output_path = f"{input_dir}{sep}output.json"
            Path(output_path).touch()

        self.output_path = Path(output_path).absolute()

        if not self.output_path.is_file():
            logger.error(f"Output file '{output_path}' does not exist")
            raise DemoOutputFileDoesNotExistException(output_path)
