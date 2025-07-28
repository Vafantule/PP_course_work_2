from typing import Optional, Dict, Any


class Vacancy:
    """
    Класс вакансии. __slots__ для экономии памяти.
    """

    __slots__ = ("_title", "_url", "_salary", "_description")

    def __init__(self, title: str, url: str, salary: Optional[Dict[str, Any]], description: Optional[str]) -> None:
        """
        Инициализирует экземпляр вакансии с проверенными атрибутами.
        """
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_description(description)

    def _validate_title(self, title: str) -> str:
        """
        Проверяет название вакансии.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название вакансии не может быть пустым.")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """
        Проверяет URL вакансии.
        """
        if not isinstance(url, str) or not url.strip():
            raise ValueError("Некорректная ссылка на вакансию.")
        return url.strip()

    def _validate_salary(self, salary: Optional[Dict[str, Any]]) -> int:
        """
        Проверяет зарплату вакансии.
        """
        if not salary or not isinstance(salary, dict):
            return 0
        return salary.get("from", 0) or salary.get("to", 0)

    def _validate_description(self, description: Optional[str]) -> str:
        """
        Проверяет описание вакансии.
        """
        return description.strip() if isinstance(description, str) and description.strip() else "Описание не указано."

    @property
    def title(self) -> str:
        """
        Получает название вакансии.
        """
        return self._title

    @property
    def url(self) -> str:
        """
        Получает URL вакансии.
        """
        return self._url

    @property
    def salary(self) -> int:
        """
        Получает зарплату вакансии.
        """
        return self._salary

    @property
    def description(self) -> str:
        """
        Получает описание вакансии.
        """
        return self._description

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Сравнивает вакансии по зарплате.
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary < other._salary

    def __eq__(self, other: "Vacancy") -> bool:
        """
        Сравнивает вакансии на предмет равенства по названию и URL.
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._title == other._title and self._url == other._url

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует вакансию в словарь.
        """
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description
        }
