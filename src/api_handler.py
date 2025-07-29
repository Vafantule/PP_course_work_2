from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class BaseVacancyAPI(ABC):
    """
    Абстрактный класс для работы с API вакансий.
    """

    @abstractmethod
    def _connect(self) -> None:
        """
        Подключение к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по ключевому слову.
        """
        pass


class HeadHunterAPI(BaseVacancyAPI):
    """
    Класс для работы с API hh.ru.
    """
    def __init__(self) -> None:
        """
        Инициализирует HeadHunterAPI с базовым URL и заголовками.
        """
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "VacancyApp/1.0"}
        self._connect()

    def _connect(self) -> None:
        """
        Приватный метод подключения к API hh.ru.
        """
        try:
            response = requests.get(self.__base_url, headers=self.__headers, timeout=10)
            if response.status_code != 200:
                raise ConnectionError(f"Ошибка подключения к API hh.ru. Код ошибки: {response.status_code}")
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения: {str(e)}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Находит вакансии с HH.ru по ключевому слову.
        """
        params = {
            "text": keyword,
            "area": "113",
            "per_page": "50"
        }
        try:
            response = requests.get(self.__base_url, headers=self.__headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or "items" not in data:
                return []
            items = data.get("items")
            if not isinstance(items, list):
                return []
            validated_items = [item for item in items if isinstance(item, dict)]
            return validated_items
        except requests.RequestException as error:
            print(f"Ошибка при получении вакансий: {str(error)}")
            return []
