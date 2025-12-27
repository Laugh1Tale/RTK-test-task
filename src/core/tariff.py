from dataclasses import dataclass, asdict


@dataclass
class Tariff:
    '''
    Класс представляющий собой тариф
    '''
    name: str  # название тарифа
    channels: str # количество каналов
    price: int  # Абонентская плата руб/мес
    speed: int  # Скорость в Мбит/c
    
    def to_excel_row(self) -> list:
        '''
        Возвращает список значений для строки Excel
        '''
        return [
            self.name,
            self.channels,
            self.speed,
            self.price
        ]