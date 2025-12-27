from dataclasses import dataclass
from typing import List


@dataclass
class BaseConfig:
    '''
    Базовая конфигурация
    '''
    BASE_URL = "https://www.rialcom.ru/internet_tariffs/"
    
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    OUTPUT_DIR: str = "output"
    OUTPUT_FILENAME: str = "rialcom_tariffs.xlsx"


@dataclass
class RegularExpressions:
    '''
    Регулярные выражения для обработки данных
    '''
    SPEED_KPBS: str = r'(\d+)\s*кбит/с'  # 100 кбит/c -> 100
    SPEED_FROM_COMMENT_HEADER: str = r'<th[^>]*>(.+?)</th>' # помогает извлечь цену из закомментированного заголовка

    PACKAGE_NAME: str = r'(.+?)\s*\(\d+\s+канал'  # Комбо Лайт (165 каналов) -> Комбо Лайт
    CHANNELS_COUNT: str = r'\((\d+)\s+канал'  # (165 каналов) -> 165

    PRICE_RUB: str = r'(\d+)\s*руб'  # 1000 руб. -> 1000


@dataclass
class Selectors:
    '''
    Селекторы для парсинга страницы
    '''
    class Category:
        '''
        Селекторы для категорий многоквартирных домов и частных домов
        '''
        APARTMENT: str = "Многоквартирные дома"
        PRIVATE: str = "Частные дома и коттеджи"

    class Internet:
        '''
        Селекторы для простых интернет тарифов.
        '''
        SECTION_TITLE: str = "Интернет"

    class InternetTV:
        '''
        Селекторы для тарифов с ТВ и интернетов
        '''
        SECTION_TITLE: str = "Интернет + Интерактивное ТВ"




@dataclass
class ExcelConfig:
    '''
    Настройки excel файла
    '''
    SHEET_NAME: str = "Тарифы RialCom"
    COLUMNS: List[str] = (
        "Название тарифа",
        "Количество каналов",
        "Скорость доступа",
        "Абонентская плата"
    )


base_config = BaseConfig()
regular_expressions = RegularExpressions()
excel_config = ExcelConfig()
selectors = Selectors()