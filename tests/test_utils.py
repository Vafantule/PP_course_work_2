from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.utils import user_interaction


@pytest.fixture
def mock_api() -> Mock:
    api = Mock()
    api.get_vacancies.return_value = [
        {
            "name": "Трубочист",
            "alternate_url": "http://example.com",
            "salary": {"from": 13},
            "snippet": {"requirement": "Прочистка труб"}
        },
        {
            "name": "Водопроводчик",
            "alternate_url": "http://plumber.com",
            "salary": {"from": 99},
            "snippet": {"requirement": "очиститель"}
        },
    ]
    return api


@pytest.fixture
def mock_file() -> Mock:
    file = Mock()
    file.get_vacancies.return_value = [
        {
            "title": "Трубочист",
            "url": "http://example.com",
            "salary": 13,
            "description": "Прочистка труб"
        },
        {
            "title": "Водопроводчик",
            "url": "http://plumber.com",
            "salary": 99,
            "description": "очиститель"
        },
    ]
    return file


@pytest.fixture
def files(mock_file: Mock) -> Dict[str, Any]:
    return {"json": mock_file, "csv": mock_file, "txt": mock_file}


@pytest.mark.parametrize("inputs, expected", [
    # 1.
    (["1", "Python", "json", "0"], {"api": 1, "add_vacancy": 1}),
    # 2.
    (["2", "json", "1", "0"], {"get_vacancies": 1}),
    # 3.
    (["3", "json", "Python", "0"], {"get_vacancies": 1}),
    # 4.
    (["4", "json", "http://py.com", "0"], {"delete_vacancy": 1}),
    # 0.
    (["0"], {}),
])
def test_user_interaction_flow(
        mock_api: Mock,
        files: Dict[str, Any],
        inputs: list[str],
        expected: Dict[str, Any]
) -> None:
    with patch("builtins.input", side_effect=inputs), patch("builtins.print") as mock_print:
        user_interaction(mock_api, files)
        if expected.get("api"):
            assert mock_api.get_vacancies.call_count == expected.get("api")
        if expected.get("add_vacancy"):
            assert files["json"].add_vacancy.call_count == expected.get("add_vacancy")
        if expected.get("get_vacancies"):
            assert files["json"].get_vacancies.call_count == expected.get("get_vacancies")
        if expected.get("delete_vacancy"):
            assert files["json"].delete_vacancy.call_count == expected.get("delete_vacancy")
        assert mock_print.call_args_list[-1][0][0].startswith("\nВыход из программы.")


def test_invalid_file_type(mock_api: Mock, files: Dict[str, Any]) -> None:
    with (patch("builtins.input", side_effect=["1", "Python", "xml", "0"]),
          patch("builtins.print") as mock_print):
        user_interaction(mock_api, files)
        assert any("Недопустимый формат файла" in call[0][0] for call in mock_print.call_args_list)


def test_invalid_choice(mock_api: Mock, files: Dict[str, Any]) -> None:
    with (patch("builtins.input", side_effect=["9", "0"]),
          patch("builtins.print") as mock_print):
        user_interaction(mock_api, files)
        assert any("Выбор не корректный" in call[0][0] for call in mock_print.call_args_list)


def test_invalid_number_top_vacancies(mock_api: Mock, files: Dict[str, Any]) -> None:
    with (patch("builtins.input", side_effect=["2", "json", "not_a_number", "0"]),
          patch("builtins.print") as mock_print):
        user_interaction(mock_api, files)
        assert any("Введите верное число вакансий" in call[0][0] for call in mock_print.call_args_list)
