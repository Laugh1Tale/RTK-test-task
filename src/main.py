from src.core.parser import Parser
from src.core.excel_writer import ExcelWriter


def main():
    # парсим данные для многоквартирных домов
    parser = Parser('apartment')
    apartment_tariffs = parser.parse_internet_tariffs()
    apartment_tv_tariffs = parser.parse_internet_tv_tariffs()

    # парсим данные для частных домов
    parser = Parser('private')
    private_tariffs = parser.parse_internet_tariffs()
    private_tv_tariffs = parser.parse_internet_tv_tariffs()

    # записываем данные в excel файл
    excel_writer = ExcelWriter()
    excel_writer.create_sheet()
    excel_writer.write_headers()

    excel_writer.write_tarriffs(apartment_tariffs)
    excel_writer.write_tarriffs(apartment_tv_tariffs)
    excel_writer.write_tarriffs(private_tariffs)
    excel_writer.write_tarriffs(private_tv_tariffs)

    excel_writer.save()


if __name__ == "__main__":
    main()