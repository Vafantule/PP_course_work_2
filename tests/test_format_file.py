import os
import tempfile
from typing import Any, Dict, Generator, List
from unittest.mock import patch

import pytest

from src.files.csv_file import CSVVacancyFile
from src.files.json_file import JSONVacancyFile
from src.files.txt_file import TXTVacancyFile


@pytest.fixture
def vacancy_data() -> List[Dict[str, Any]]:
    return [
        {
            "title": "Водопроводчик",
            "url": "http://plumber.com",
            "salary": 99,
            "description": "очиститель"
        },
        {
            "title": "Написатель",
            "url": "url_new",
            "salary": 0,
            "description": "писатель"
        },
    ]


@pytest.fixture
def temp_json_file() -> Generator[str, Any, None]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp:
        yield temp.name
    os.remove(temp.name)


@pytest.fixture
def temp_csv_file() -> Generator[str, Any, None]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp:
        yield temp.name
    os.remove(temp.name)


@pytest.fixture
def temp_txt_file() -> Generator[str, Any, None]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp:
        yield temp.name
    os.remove(temp.name)


@pytest.fixture
def json_connector(temp_json_file: str) -> JSONVacancyFile:
    return JSONVacancyFile(filename=temp_json_file)


@pytest.fixture
def csv_connector(temp_csv_file: str) -> CSVVacancyFile:
    return CSVVacancyFile(filename=temp_csv_file)


@pytest.fixture
def txt_connector(temp_txt_file: str) -> TXTVacancyFile:
    return TXTVacancyFile(filename=temp_txt_file)


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_add_vacancy(connector_name: str, request: pytest.FixtureRequest,
                     vacancy_data: List[Dict[str, Any]]) -> None:
    connector = request.getfixturevalue(connector_name)
    connector.add_vacancy(vacancy_data)
    result = connector.get_vacancies({})
    assert len(result) == 2
    assert result[0]["title"] == "Водопроводчик"
    assert result[1]["url"] == "url_new"


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_get_vacancy_by_keyword(connector_name: str, request: pytest.FixtureRequest,
                                vacancy_data: List[Dict[str, Any]]) -> None:
    connector = request.getfixturevalue(connector_name)
    connector.add_vacancy(vacancy_data)
    result = connector.get_vacancies({"keyword": "Написатель"})
    assert len(result) == 1
    assert result[0]["title"] == "Написатель"


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_delete_vacancy(connector_name: str, request: pytest.FixtureRequest,
                        vacancy_data: List[Dict[str, Any]]) -> None:
    connector = request.getfixturevalue(connector_name)
    connector.add_vacancy(vacancy_data)
    connector.delete_vacancy("http://plumber.com")
    result = connector.get_vacancies({})
    assert len(result) == 1
    assert result[0]["title"] == "Написатель"


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_no_duplicate_vacancy(connector_name: str, request: pytest.FixtureRequest,
                              vacancy_data: List[Dict[str, Any]]) -> None:
    connector = request.getfixturevalue(connector_name)
    connector.add_vacancy(vacancy_data)
    connector.add_vacancy(vacancy_data[0])
    result = connector.get_vacancies({})
    assert len(result) == 2


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_add_vacancy_patch(connector_name: str, request: pytest.FixtureRequest,
                           vacancy_data: List[Dict[str, Any]]) -> None:
    connector = request.getfixturevalue(connector_name)
    with patch.object(connector, "add_vacancy", return_value=None) as mock_add:
        connector.add_vacancy(vacancy_data)
        mock_add.assert_called_once()


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_get_vacancy_patch(connector_name: str, request: pytest.FixtureRequest) -> None:
    connector = request.getfixturevalue(connector_name)
    with patch.object(connector, "get_vacancies", return_value=[{"title": "Mock"}]) as mock_get:
        result = connector.get_vacancies({"keyword": 'any'})
        mock_get.assert_called_once()
        assert result == [{"title": 'Mock'}]


@pytest.mark.parametrize("connector_name", [
    "json_connector",
    "csv_connector" ,
    "txt_connector" ,
])
def test_delete_vacancy_patch(connector_name: str, request: pytest.FixtureRequest) -> None:
    connector = request.getfixturevalue(connector_name)
    with patch.object(connector, "delete_vacancy", return_value=None) as mock_delete:
        connector.delete_vacancy("http://any.com")
        mock_delete.assert_called_once()
