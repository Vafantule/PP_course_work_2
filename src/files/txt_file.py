from src.files.base_file import BaseFileVacancyWork
from typing import List, Dict, Any
import os


class TXTVacancyFile(BaseFileVacancyWork):
    """
    Класс для работы с TXT-файлом.
    """

    def __init__(self, filename: str = "data/vacancies.txt") -> None:
        """
        Инициализирует TXT с именем файла.
        """
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                file.write("")

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Загружает вакансии из TXT-файла.
        """
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                vacancies = []
                for line in lines:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        title, url, salary, description = parts
                        vacancies.append({
                            "title": title,
                            "url": url,
                            "salary": int(salary) if salary.isdigit() else 0,
                            "description": description
                        })
                return vacancies
        except FileNotFoundError:
            return []

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавляет вакансию в TXT-файл, если она еще не существует.
        """
        vacancies = self._load_vacancies()
        if not any(vacancy_in_selection["url"] == vacancy["url"] for vacancy_in_selection in vacancies):
            with open(self.__filename, "a", encoding="utf-8") as file:
                file.write(f"{vacancy['title']}|{vacancy['url']}|{vacancy['salary']}|{vacancy['description']}\n")

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
        Удаляет вакансию по URL из TXT-файла.
        """
        vacancies = self._load_vacancies()
        vacancies = [vacancy for vacancy in vacancies if vacancy["url"] != url]
        with open(self.__filename, "w", encoding="utf-8") as file:
            for vacancy in vacancies:
                file.write(f"{vacancy['title']}|{vacancy['url']}|{vacancy['salary']}|{vacancy['description']}\n")