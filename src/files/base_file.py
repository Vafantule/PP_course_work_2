from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseFileVacancyWork(ABC):
    """
    Абстрактный базовый класс для операций чтения вакансий из файла.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: List[Dict[str, Any]]) -> None:
        """
        Добавляет вакансию в хранилище.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Находит вакансии на основе критериев.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, url: str) -> None:
        """
        Удаляет вакансию по URL.
        """
        pass
