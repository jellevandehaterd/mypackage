import logging
import os
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner

from mypackage.mypackage import configure_logging
from mypackage.mypackage import main
from tests.helpers import AnyArg


@pytest.fixture(autouse=True)
def chdir_to_tmp_path(tmp_path: Path) -> None:
    # To simulate the CLI as close to the real-world as possible, we change the working directory
    # to a temporary directory so that the commands can be executed using relative paths
    os.chdir(str(tmp_path))


class TestDemo:
    def test__demo(self, caplog: LogCaptureFixture) -> None:
        # Arrange
        runner = CliRunner()

        caplog.set_level(10)

        # Act
        result = runner.invoke(main, ["demo"])

        # Assert
        assert 0 == result.exit_code
        assert "Attempting to demo!" in caplog.messages


class TestSetLogLevel:
    @pytest.mark.parametrize(
        "q,v,expected_level",
        [
            (0, 3, logging.DEBUG - 10),
            (0, 2, logging.DEBUG),
            (0, 1, logging.INFO),
            (0, 0, logging.WARNING),
            (50, 50, logging.WARNING),
            (1, 0, logging.ERROR),
            (2, 1, logging.ERROR),
            (2, 0, logging.CRITICAL),
            (3, 0, logging.CRITICAL + 10),
        ],
    )
    def test__set_log_level__sets_expected_log_level(
        self, v: int, q: int, expected_level: int, mocker
    ) -> None:
        # Arrange
        mocker.patch.object(logging, "basicConfig")

        # Act
        configure_logging(verbosity=v, quiet=q)

        # Assert
        logging.basicConfig.assert_called_with(level=expected_level, format=AnyArg())

    def test__set_log_level__defaults_to_basic_format(self, mocker) -> None:
        # Arrange
        mocker.patch.object(logging, "basicConfig")

        # Act
        configure_logging(0, 0, False)

        # Assert
        logging.basicConfig.assert_called_with(
            level=AnyArg(), format=logging.BASIC_FORMAT
        )

    def test__set_log_level__json_sets_different_format(self, mocker) -> None:
        # Arrange
        mocker.patch.object(logging, "basicConfig")

        # Act
        configure_logging(0, 0, True)

        # Assert
        format_result: str = logging.basicConfig.call_args[1]["format"]

        assert format_result != logging.BASIC_FORMAT
