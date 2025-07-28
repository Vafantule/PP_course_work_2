from typing import Dict

from src.api_handler import HeadHunterAPI
from src.files.base_file import BaseFileVacancyWork
from src.vacancy import Vacancy


def user_interaction(api: HeadHunterAPI, files: Dict[str, BaseFileVacancyWork]) -> None:
    """
    Предоставляет консольный пользовательский интерфейс для взаимодействия с данными о вакансиях.
    """
    while True:
        print("\nМеню:")
        print("1. Поиск и сохранение вакансий по ключевому слову")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Показать вакансии по ключевому слову в описании")
        print("4. Удалить вакансию по URL")
        print("0. Выйти")

        choice = input("Выберите действие (1-5): ")
        if choice == "1":
            keyword = input("Введите запрос по слову: ")
            file_type = input("Выберите формат файла для обработки (json/csv/txt): ").lower()
            if file_type not in files:
                print("Недопустимый формат файла. Доступные варианты: json, csv, txt")
                continue

            vacancies = api.get_vacancies(keyword)
            if not vacancies:
                print("Не найдены вакансии или произошла ошибка.")
                continue

            for index in vacancies:
                try:
                    vacancy = Vacancy(
                        title=index.get("name", ""),
                        url=index.get("alternate_url", ""),
                        salary=index.get("salary"),
                        description=index.get("snippet", {}).get("requirement", "Not specified")
                    )
                    files[file_type].add_vacancy(vacancy.to_dict())
                    print(f"Добавлены вакансии: {vacancy.title}")
                except ValueError as error:
                    print(f"Пропуск недействительных вакансий: {str(error)}")

        elif choice == "2":
            file_type = input("Выберите формат файла для обработки (json/csv/txt): ").lower()
            if file_type not in files:
                print("Недопустимый формат файла. Доступные варианты: json, csv, txt")
                continue
            try:
                number = int(input("Введите число вакансий для вывода: "))
                vacancies = files[file_type].get_vacancies({})
                sorted_vacancies = sorted(vacancies, key=lambda element: element.get("salary"), reverse=True)[:number]

                for vacancy in sorted_vacancies:
                    salary = vacancy.get("salary") if vacancy.get("salary") > 0 else "Нет данных"
                    print(f"\nНазвание: {vacancy.get('title')}")
                    print(f"URL: {vacancy.get('url')}")
                    print(f"Зарплата: {salary}")
                    print(f"Описание: {vacancy.get('description')}")
            except ValueError:
                print("Введите верное число вакансий для отбора.")

        elif choice == "3":
            file_type = input("Выберите формат файла для обработки (json/csv/txt): ").lower()
            if file_type not in files:
                print("Недопустимый формат файла. Доступные варианты: json, csv, txt")
                continue

            keyword = input("Введите слово для поиска в вакансиях: ")
            vacancies = files[file_type].get_vacancies({"keyword" : keyword})

            for vacancy in vacancies:
                salary = vacancy.get("salary") if vacancy.get("salary") > 0 else "Нет данных"
                print(f"\nНазвание: {vacancy.get('title')}")
                print(f"URL: {vacancy.get('url')}")
                print(f"Зарплата: {salary}")
                print(f"Описание: {vacancy.get('description')}")

        elif choice == "4":
            file_type = input("Выберите формат файла для обработки (json/csv/txt): ").lower()
            if file_type not in files:
                print("Недопустимый формат файла. Доступные варианты: json, csv, txt")
                continue

            url = input("Введите URL вакансии для удаления: ")
            files[file_type].delete_vacancy(url)
            print(f"Вакансии по ссылке URL удалены из {file_type} файла.")

        elif choice == "0":
            print("\nВыход из программы.")
            break

        else:
            print("\nВыбор не корректный. Выберите из 1-5.")
