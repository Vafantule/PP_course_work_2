from typing import Any, Dict, Optional

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def valid_salary() -> Dict[str, Any]:
    return {"from": 1, "to": 2}


@pytest.fixture
def vacancy_data(valid_salary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": "Трубочист",
        "url": "http://example.com",
        "salary": valid_salary,
        "description": "Прочистка труб"
    }


@pytest.fixture
def vacancy(vacancy_data: Dict[str, Any]) -> Vacancy:
    return Vacancy(
        title=vacancy_data.get("title", ""),
        url=vacancy_data.get("url", ""),
        salary=vacancy_data["salary"],
        description=vacancy_data.get("description", ""),
    )


@pytest.mark.parametrize("title, url, salary, description, expected", [
    ("Водопроводчик", "http://plumber.com", {"from": 99}, "Очиститель", 99),
    ("Учитель", "http://teacher.net", {"to": 199}, "Образование", 199),
    ("Столяр", "http://carpenter.ua", None, "Обработка", 0),
    ("Инженер", "http://engineer.us", {}, "Обслуживание", 0),
])
def test_salary_parsing(
        title: str,
        url: str,
        salary: Optional[Dict[str, Any]],
        description: str, expected: int) -> None:
    vacancy = Vacancy(title, url, salary, description)
    assert vacancy.salary == expected


def test_title_validation() -> None:
    with pytest.raises(ValueError):
        Vacancy("", "http://test.com", None, "Описание")
    with pytest.raises(ValueError):
        Vacancy("  ", "http://test.com", None, "Описание")


def test_url_validation() -> None:
    with pytest.raises(ValueError):
        Vacancy("Трубочист", "", None, "Описание")
    with pytest.raises(ValueError):
        Vacancy("Трубочист", "  ", None, "Описание")


@pytest.mark.parametrize("description, expected", [
    ("Описание", "Описание"),
    ("  ", "Описание не указано."),
    (None, "Описание не указано."),
])
def test_description_validation(description: Optional[str], expected: str) -> None:
    vacancy = Vacancy("Трубочист", "http://example.com", None, description)
    assert vacancy.description == expected


def test_properties(vacancy: Vacancy, vacancy_data: Dict[str, Any]) -> None:
    assert vacancy.title == vacancy_data.get("title", "")
    assert vacancy.url == vacancy_data.get("url", "")
    assert vacancy.salary == vacancy_data["salary"]["from"]
    assert vacancy.description == vacancy_data.get("description", "")


def test_to_dict(vacancy: Vacancy, vacancy_data: Dict[str, Any]) -> None:
    dict_for_test = vacancy.to_dict()
    assert isinstance(dict_for_test, dict)
    assert dict_for_test.get("title", "") == vacancy_data.get("title", "")
    assert dict_for_test.get("url", "") == vacancy_data.get("url", "")
    assert dict_for_test.get("salary", "") == vacancy_data["salary"]["from"]
    assert dict_for_test.get("description", "") == vacancy_data.get("description", "")


def test_comparison_operators() -> None:
    vacancy_1 = Vacancy("Водопроводчик", "url_1", {"from": 99}, "Очиститель")
    vacancy_2 = Vacancy("Учитель", "url_2", {"from": 199}, "Образование")
    assert vacancy_1 < vacancy_2
    assert vacancy_2 > vacancy_1
    assert not vacancy_1 > vacancy_2
    assert not vacancy_2 < vacancy_1


def test_equality_operator() -> None:
    vacancy_1 = Vacancy("Водопроводчик", "url_1", {"from": 99}, "Очиститель")
    vacancy_2 = Vacancy("Водопроводчик", "url_1", {"from": 199}, "Обеззараживатель")
    vacancy_3 = Vacancy("Столяр", "url_2", {"from": 99}, "Обработка")
    assert vacancy_1 == vacancy_2
    assert vacancy_1 != vacancy_3


def test_comparison_with_non_vacancy() -> None:
    vacancy_1 = Vacancy("Водопроводчик", "url_1", {"from": 99}, "Очиститель")
    assert vacancy_1.__lt__("не вакансия") is NotImplemented
    assert vacancy_1.__gt__("не вакансия") is NotImplemented
    assert vacancy_1.__eq__("не вакансия") is NotImplemented
