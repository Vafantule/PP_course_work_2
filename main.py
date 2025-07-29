from src.api_handler import HeadHunterAPI
from src.files.csv_file import CSVVacancyFile
from src.files.json_file import JSONVacancyFile
from src.files.txt_file import TXTVacancyFile
from src.utils import user_interaction


def main() -> None:
    """
    Основная точка входа программы. Инициализирует обработчик API и классы хранилища,
    и запускает цикл взаимодействия с пользователем.
    """
    api = HeadHunterAPI()
    json_file = JSONVacancyFile()
    csv_file = CSVVacancyFile()
    txt_file = TXTVacancyFile()

    files = {
        "json": json_file,
        "csv": csv_file,
        "txt": txt_file
    }

    user_interaction(api, files)


if __name__ == "__main__":
    main()
