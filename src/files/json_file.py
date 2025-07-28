from src.files.base_file import BaseFileVacancyWork
from typing import List, Dict, Any, Union
import json
import os


class JSONVacancyFile(BaseFileVacancyWork):
    """
    Класс для работы с JSON-файлом.
    """
    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """
        Инициализирует JSON с именем файла.
        """
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Загружает вакансии из JSON-файла.
        """
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # def add_vacancy(self, vacancy: List[Dict[str, Any]]) -> None:
    #     """
    #     Добавляет вакансию в JSON-файл, если она еще не существует.
    #     """
    #     vacancies = self._load_vacancies()
    #     urls = {vacancy.get("url") for vacancy in vacancies}
    #     new_vacancies = [vacancy for vacancy in vacancies if vacancy.get("url") not in urls]
    #     with open(self.__filename, "w", encoding="utf-8") as file:
    #         json.dump(new_vacancies, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancies: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
        """
        Добавляет вакансию в JSON-файл, если она еще не существует.
        """
        # Normalize input to a list
        vacancy_list = [vacancies] if isinstance(vacancies, dict) else vacancies
        existing_vacancies = self._load_vacancies()
        existing_urls = {v["url"] for v in existing_vacancies if isinstance(v, dict) and "url" in v}
        # Filter out duplicates based on URL
        new_vacancies = [v for v in vacancy_list if isinstance(v, dict) and v.get("url") not in existing_urls]
        # Overwrite with the new list of vacancies
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(new_vacancies, f, ensure_ascii=False, indent=2)


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
        vacancies = [vacancy for vacancy in vacancies if vacancy["url"] != url]
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)
