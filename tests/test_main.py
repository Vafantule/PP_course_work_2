from unittest.mock import Mock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from main import main


@pytest.fixture
def mock_api() -> Mock:
    return Mock()


@pytest.fixture
def mock_json_file() -> Mock:
    return Mock()


@pytest.fixture
def mock_csv_file() -> Mock:
    return Mock()


@pytest.fixture
def mock_txt_file() -> Mock:
    return Mock()


def test_main_user_interaction(
        mock_api: Mock,
        mock_json_file: Mock,
        mock_csv_file: Mock,
        mock_txt_file: Mock,
) -> None:
    with (patch("main.HeadHunterAPI", return_value=mock_api),
          patch("main.JSONVacancyFile", return_value=mock_json_file),
          patch("main.CSVVacancyFile", return_value=mock_csv_file),
          patch("main.TXTVacancyFile", return_value=mock_txt_file),
          patch("main.user_interaction") as mock_user_interaction):
        main()
        mock_user_interaction.assert_called_once()
        args, kwargs = mock_user_interaction.call_args
        assert args[0] is mock_api
        assert args[1]["json"] is mock_json_file
        assert args[1]["csv"] is mock_csv_file
        assert args[1]["txt"] is mock_txt_file


def test_main_entrypoint(monkeypatch: MonkeyPatch) -> None:
    import main
    monkeypatch.setattr(main, "__name__", "__main__")
    with patch("main.main") as mock_main:
        if main.__name__ == "__main__":
            main.main()
        assert mock_main.call_count == 1
