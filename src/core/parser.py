from bs4 import BeautifulSoup, Comment
import requests
from .tariff import Tariff
from ..config import selectors, regular_expressions, base_config
from typing import List, Tuple
import re

class Parser:
    '''
    Класс парсер
    '''
    def __init__(self, category):
        response = requests.get(base_config.BASE_URL) 
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.category = category

    
    def parse_internet_tariffs(self):
        '''
        Парсит интернет тарифы
        '''
        tariffs = []
        if self.category == "apartment":
            expression = selectors.Category.APARTMENT
        elif self.category == "private":
            expression = selectors.Category.PRIVATE
        else:
            return tariffs
        button = self.soup.find("button", text=lambda t: t and expression in t.strip())
        if not button:
            return tariffs
        internet_section = button.find_next("div", text=lambda t: t and selectors.Internet.SECTION_TITLE in t.strip())
        if not internet_section:
            return tariffs
        table = internet_section.find_next('table')
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    name = cols[0].text.strip()
                    price = cols[1].text.strip()
                    speed = cols[3].text.strip()
                    clean_name = self._clean_text(name)
                    clean_price = self._extract_price(price)
                    converted_speed = self._convert_speed(speed)
                    tarrif = Tariff(
                        name = clean_name,
                        channels = "null",
                        price = clean_price,
                        speed = converted_speed,
                    )
                    tariffs.append(tarrif)
        return tariffs
    

    def parse_internet_tv_tariffs(self):
        '''
        Парсит комбинированные тарифы
        '''
        tariffs = []
        if self.category == "apartment":
            expression = selectors.Category.APARTMENT
        elif self.category == "private":
            expression = selectors.Category.PRIVATE
        else:
            return tariffs
        button = self.soup.find("button", text=lambda t: t and expression in t.strip())
        if not button:
            return tariffs
        internet_section = button.find_next = self.soup.find('div', text=lambda t: t and selectors.InternetTV.SECTION_TITLE in t.strip())
        if not internet_section:
            return tariffs
        table = internet_section.find_next('table')
        speeds = self._extract_speeds_from_table(table)
        rows = table.select('tbody tr')
        for index, row in enumerate(rows, 1):
            package_elem = row.select_one("td.text-left")
            if not package_elem:
                continue
                
            package_text = self._clean_text(package_elem.text)
            package_name, channels = self._extract_package_info(package_text)
                
            prices = self._extract_all_prices(row)
            for i, price in enumerate(prices):                  
                    tariff_name = self._generate_tv_tariff_name(
                        package_name, speeds[i]
                    )
                    
                    tariff = Tariff(
                        name = tariff_name,
                        price = price,
                        speed = speeds[i],
                        channels = channels,
                    )
                    
                    tariffs.append(tariff)
        return tariffs
    
    
    def _extract_speeds_from_table(self, table) -> List[int]:
        '''
        Извлекает скорости интернета из заголовка таблицы
        '''
        speeds = []

        headers = table.find('thead').find('tr')

        for header in headers:
            if isinstance(header, Comment):
                comment_text = str(header)
                th_match = re.search(regular_expressions.SPEED_FROM_COMMENT_HEADER, comment_text)
                header = th_match.group(1).strip()
            else:
                header = header.get_text(strip = True)
            match = re.search(r'(\d+)', header)
            if match:
                speeds.append(int(match.group(1)))

        return speeds
    

    def _clean_text(self, text: str) -> str:
        '''
        Очищает текст от лишних пробелов и *
        '''
        text = text.replace('*', '')
        text = text.strip()
        text = " ".join(text.split())
        return text

    
    def _extract_price(self, text: str) -> str:
        '''
        Извлекает и форматирует цену
        '''
        match = re.search(regular_expressions.PRICE_RUB, text)
        return match.group(1)
    

    def _convert_speed(self, text: str) -> str:
        '''
        Конвертирует скорость в Мбит/с
        '''
        kbps_match = re.search(regular_expressions.SPEED_KPBS, text)
        return int(float(kbps_match.group(1)) / 1000)
    

    def _extract_package_info(self, text: str) -> Tuple[str, int]:
        '''
        Извлекает название пакета и количество каналов
        '''
        channels_match = re.search(regular_expressions.CHANNELS_COUNT, text)
        channels = int(channels_match.group(1)) if channels_match else None
        
        name_match = re.search(regular_expressions.PACKAGE_NAME, text)
        package_name = name_match.group(1).strip() if name_match else None
        
        return package_name, channels
    

    def _extract_all_prices(self, row):
        '''
        извлекает все цены из строки таблицы
        '''
        all_prices = []
        for element in row.children:
            if element.name == 'td':
                if 'text-left' not in element.get('class', []):
                    all_prices.append(element.get_text(strip=True))
        
            elif isinstance(element, Comment):
                comment_text = str(element)
                if '<td>' in comment_text:
                    temp_soup = BeautifulSoup(comment_text, 'html.parser')
                    td_in_comment = temp_soup.find('td')
                    if td_in_comment:
                        all_prices.append(td_in_comment.get_text(strip=True))
    
        return all_prices
    

    def _generate_tv_tariff_name(self, package_name: str, speed: int) -> str:
        '''
        Генерирует название комбинированных тарифов
        '''
        if self.category == "apartment":
            return f"{package_name} + РиалКом Интернет {speed} + ТВ"
        elif self.category == "private":
            return f"{package_name} + РиалКом Интернет {speed} + ТВ_ч"