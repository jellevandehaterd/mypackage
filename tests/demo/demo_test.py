import os
from os.path import sep
from pathlib import Path
import pytest
from _pytest.logging import LogCaptureFixture

from mypackage.demo.demo import Demo, DemoInputFileDoesNotExistException, DemoOutputFileDoesNotExistException


class TestDemo:
    @pytest.mark.parametrize(
        "input_path",
        ["input.txt"]
    )
    def test__init__throws_exception_if_input_path_does_not_exist(self, tmp_path: Path, input_path: str) -> None:
        with pytest.raises(DemoInputFileDoesNotExistException) as context:
            Demo(f"{tmp_path}{sep}{input_path}")
        assert (
                f"Input file '{tmp_path}{sep}{input_path}' does not exist"
                == context.value.message
        )

    @pytest.mark.parametrize(
        "input_path, output_path",
        [("input.txt", "output.json")]
    )
    def test__init__throws_exception_if_output_path_does_not_exist(self, tmp_path: Path, input_path: str, output_path: str) -> None:
        with pytest.raises(DemoOutputFileDoesNotExistException) as context:

            Path(f"{tmp_path}{sep}{input_path}").touch()

            os.chdir(str(tmp_path))

            Demo(f"{tmp_path}{sep}{input_path}", f"{tmp_path}{sep}{output_path}")
        assert (
                f"Output file '{tmp_path}{sep}{output_path}' does not exist"
                == context.value.message
        )

    @pytest.mark.parametrize(
        "input_path",
        ["input.txt"]
    )
    def test__init__sets_input_path_properly(self, tmp_path: Path, input_path: str) -> None:
        Path(f"{tmp_path}{sep}{input_path}").touch()

        os.chdir(str(tmp_path))

        demo = Demo(f"{tmp_path}{sep}{input_path}")

        assert f"{tmp_path}{sep}{input_path}" == str(demo.input_path)
