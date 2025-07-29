from typing import List, Dict, Any
from unittest.mock import patch, Mock

import pytest
import requests

from src.api_handler import BaseVacancyAPI, HeadHunterAPI


class FakeVacancyAPI(BaseVacancyAPI):
    def _connect(self) -> None:
        self.connect = True

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Трубочист",
                 "url": "http://example.com",
                 "salary": 13,
                 "description": "Прочистка труб"
            }
        ]


@pytest.fixture
def fake_api() -> FakeVacancyAPI:
    return FakeVacancyAPI()


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    return HeadHunterAPI()


def test_fake_connect(fake_api: FakeVacancyAPI) -> None:
    fake_api._connect()
    assert hasattr(fake_api, "connect")
    assert fake_api.connect is True


@pytest.mark.parametrize("keyword", ["Трубочист", "Водопроводчик", ""])
def test_fake_get_vacancies(fake_api: FakeVacancyAPI, keyword: str) -> None:
    vacancies = fake_api.get_vacancies(keyword)
    assert isinstance(vacancies, list)
    assert isinstance(vacancies[0], dict)
    assert "title" in vacancies[0]


def test_hh_connect_patch() -> None:
    with patch("src.api_handler.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        api = HeadHunterAPI()
        api._connect()
        mock_get.assert_called()


@pytest.mark.parametrize("keyword", ["Трубочист", "Водопроводчик", ""])
def test_hh_get_vacancies_patch(keyword: str) -> None:
    with patch("src.api_handler.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
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
        }
        mock_get.return_value = mock_response
        api = HeadHunterAPI()
        vacancies = api.get_vacancies(keyword)
        assert isinstance(vacancies, list)
        assert isinstance(vacancies[0], dict)
        assert "title" in vacancies[0]


def test_hh_get_vacancies_error_patch() -> None:
    with patch("src.api_handler.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.side_effect = requests.ConnectionError("Ошибка подключения к API hh.ru")
        mock_get.return_value = mock_response
        api = HeadHunterAPI()
        result = api.get_vacancies("Трубочист")
        assert result == []
