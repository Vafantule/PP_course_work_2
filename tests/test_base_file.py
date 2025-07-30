from typing import Any, Dict, List
from unittest.mock import patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.files.base_file import BaseFileVacancyWork


class FakeFileVacancyWork(BaseFileVacancyWork):
    def add_vacancy(self, vacancy: List[Dict[str, Any]]) -> None:
        self._add = vacancy

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"title": "Трубочист",
             "url": "http://example.com",
             "salary": 13,
             "description": "Прочистка труб"}
        ]

    def delete_vacancy(self, url: str) -> None:
        self._delete = url


@pytest.fixture
def fake_connector() -> FakeFileVacancyWork:
    return FakeFileVacancyWork()


def test_add_vacancy(fake_connector: FakeFileVacancyWork) -> None:
    data = [
        {"title": "Водопроводчик",
         "url": "http://plumber.com",
         "salary": 99,
         "description": "очиститель"}
    ]
    fake_connector.add_vacancy(data)
    assert hasattr(fake_connector, "_add")
    assert fake_connector._add == data


def test_get_vacancy(fake_connector: FakeFileVacancyWork) -> None:
    resource = fake_connector.get_vacancies({"keyword": "трубо"})
    assert isinstance(resource, list)
    assert isinstance(resource[0], dict)
    assert resource[0]["title"] == "Трубочист"


@pytest.mark.parametrize("url", [
    "http://test.com",
    "",
    None
])
def test_delete_vacancy(fake_connector: FakeFileVacancyWork, url: str) -> None:
    fake_connector.delete_vacancy(url)
    assert hasattr(fake_connector, "_delete")
    assert fake_connector._delete == url


def test_add_vacancy_patch(monkeypatch: MonkeyPatch, fake_connector: FakeFileVacancyWork) -> None:
    with patch.object(fake_connector, "add_vacancy", return_value=None) as mock_add:
        fake_connector.add_vacancy([
            {
                "title": "Написатель",
                "url": "url_new",
                "salary": 0,
                "description": "писатель"
            }
        ])
        mock_add.assert_called_once()


def test_get_vacancy_patch(monkeypatch: MonkeyPatch, fake_connector: FakeFileVacancyWork) -> None:
    with patch.object(fake_connector, "get_vacancies", return_value=[{"title": "Тесты"}]) as mock_get:
        result = fake_connector.get_vacancies({"keyword": "тесты"})
        mock_get.assert_called_once()
        assert result == [{"title": "Тесты"}]


def test_delete_vacancy_patch(monkeypatch: MonkeyPatch, fake_connector: FakeFileVacancyWork) -> None:
    with patch.object(fake_connector, "delete_vacancy", return_value=None) as mock_delete:
        fake_connector.delete_vacancy("http://todelete.com")
        mock_delete.assert_called_once()
