import csv
import os
from typing import Any, Dict, List, Union

from src.files.base_file import BaseFileVacancyWork


class CSVVacancyFile(BaseFileVacancyWork):
    """
    Класс для работы с CSV-файлом.
    """

    def __init__(self, filename: str = "data/vacancies.csv") -> None:
        """
        Инициализирует CSV с именем файла.
        """
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["title", "url", "salary", "description"])
                writer.writeheader()

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Загружает вакансии из CSV-файла.
        """
        try:
            with open(self.__filename, "r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                vacancies = list(reader)
                for vacancy in vacancies:
                    vacancy["salary"] = int(vacancy["salary"]) if vacancy["salary"].isdigit() else 0
                return vacancies
        except (FileNotFoundError, csv.Error):
            return []

    def add_vacancy(self, vacancies: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
        """
        Добавляет вакансию в CSV-файл, если она еще не существует.
        """
        vacancy_list = [vacancies] if isinstance(vacancies, dict) else vacancies
        existing_vacancies = self._load_vacancies()
        urls = {vacancy.get("url") for vacancy in existing_vacancies if
                isinstance(vacancy, dict) and "url" in vacancy}
        new_vacancies = [vacancy for vacancy in vacancy_list if
                         isinstance(vacancy, dict) and vacancy.get("url") not in urls]
        with open(self.__filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "url", "salary", "description"])
            writer.writeheader()
            writer.writerows(new_vacancies)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Находит вакансии, соответствующие заданным критериям.
        """
        vacancies = self._load_vacancies()
        keyword = criteria.get("keyword", "").lower()
        if not keyword:
            return vacancies
        return [
            vacancy for vacancy in vacancies
            if keyword in vacancy.get("title", "").lower() or keyword in vacancy.get("description", "").lower()
        ]

    def delete_vacancy(self, url: str) -> None:
        """
        Удаляет вакансию по URL из JSON-файла.
        """
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v["url"] != url]
        with open(self.__filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "url", "salary", "description"])
            writer.writeheader()
            writer.writerows(vacancies)
