from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from typing import List
import enum
import re

#region Модели Enum и Валидаторы 

class OffersInfoLastMilePolicy(enum.Enum):
    """
    Класс для расчета интервала доставки
    Доставка до двери в указанный интервал - Default: time_interval

    time_interval: доставка до двери в указанный интервал
    self_pickup: доставка до пункта выдачи
    """
    time_interval = 'time_interval'
    self_pickup = 'self_pickup'

class PickupStationType(enum.Enum):
    """
    PickupStationType: Тип ПВЗ
    pickup_point — пункт выдачи заказов;
    terminal — постомат;
    warehouse — сортировочный центр;
    """
    pickup_point = 'pickup_point'
    terminal ='terminal'
    warehouse = 'warehouse'

class  PaymentMethod(enum.Enum):
    """
    PaymentMethod: Методы оплаты
    already_paid — уже оплачено;
    card_on_receipt — оплата картой при получении;
    """
    already_paid = 'already_paid'
    card_on_receipt = 'card_on_receipt'

class DestinationRequestNode(enum.Enum):
    """
    Вариант указания целевой точки доставки
    type: string
    Тип целевой точки. Для доставки до двери — custom_location (2), для доставки до ПВЗ — platform_station (1)
    """
    platform_station = 'platform_station' 

class LastMilePolicy(enum.Enum):
    """
    lastMilePolicy: Политика последней мили
    self_pickup - доставка до пункта выдачи
    time_interval - доставка до двери в указанный интервал
    """
    self_pickup = 'self_pickup'
    time_interval = 'time_interval'  

class ContactPerson(BaseModel):
    """
    contactPerson: контактное лицо
    first_name*: str - Имя контактного лица
    phone*: str - Телефон контактного лица в формате +7xxxxxxxxxx
    email: str - Email контактного лица
    """
    first_name: str
    phone: str = Field(..., description="Телефон в формате +7XXXXXXXXXX")
    email: Optional[EmailStr] = None 
    

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        """Валидация формата телефона: +7XXXXXXXXXX"""
        pattern = r"^\+7\d{10}$"
        if not re.match(pattern, value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX")
        return value

class TimeIntervalUTC(BaseModel):
    """
    timeIntervalUTC: информация о временном интервале
    start_utc: datetime - UTC timestamp для нижней границы интервала
    end_utc: datetime - UTC timestamp для верхней границы интервала
    """
    start_utc: datetime = Field(..., description="UTC timestamp начала интервала")
    end_utc: datetime = Field(...,  description="UTC timestamp конца интервала")

    class Config:
        allow_population_by_field_name = True
        
#endregion

class PricingDestinationNode(BaseModel):
    """
    Информация о точке получения заказа
    address	Type: string
    Адрес получения с указанием города, улицы и номера дома.
    Номер квартиры, подъезда и этаж указывать не нужно

        Example: Санкт-Петербург, Большая Монетная улица, 1к1А

    platform_station_id	Type: any
    ID ПВЗ или постамата, зарегистрированного в платформе, в который нужна доставка
"""
    address: str 
    platform_station_id: str

class PricingSourceNode(BaseModel):
    """
    Класс для указания точки отправления заказа
    platform_station_id: str
    ID склада отправки, зарегистрированного в платформе
    """
    platform_station_id: str


class BillingInfo(BaseModel):
    """
    billingInfo: информация о платеже
    payment_method: already_paid - Метод оплаты
    delivery_cost: int - Сумма, которую нужно взять с получателя за доставку. Актуально только для заказов с постоплатой (тип оплаты card_on_receipt)
    variable_delivery_cost_for_recipient - Список стоимостей доставки в зависимости от суммы выкупленных товаров.
    Позволяет управлять скидками на доставку для получателя. Скидка применяется только для заказов с постоплатой и частичным выкупом.
    """
    payment_method: PaymentMethod
    delivery_cost: Optional[int] = None
    variable_delivery_cost_for_recipient: Optional[List["VariableDeliveryCostForRecipientItem"]] = None

BillingInfo.model_rebuild()



class VariableDeliveryCostForRecipientItem(BaseModel):
    """
    Возможность предоставления скидки на доставку в зависимости от суммы выкупленных товаров.
    delivery_cost: int - Стоимость доставки до применения скидки (min_value:0)
    min_cost_of_accepted_items: int - Стоимость выкупленных товаров, при достижении которой применяется скидка (min_value:1)
    """
    delivery_cost: int
    min_cost_of_accepted_items: int

  
class ItemBillingDetails(BaseModel):
    """
    assessed_unit_price*: int - Оценочная цена за единицу товара (передается в копейках)
    unit_price*: int - Цена за единицу товара (передается в копейках)
    nds: int : Значение НДС. Допустимые значения — 0, 5, 7, 10, 20. Если заказ без НДС, передавайте значение -1
    """
    assessed_unit_price: int
    unit_price: int
    nds: Optional[int] = -1

class RequestResourceItem(BaseModel):
    """
    requestResourceItem: информация о товаре
    article*: string - Артикул
    billing_details*: ItemBillingDetails - Данные по биллингу для предмета
    count*: int - Количество
    name*: str - Название
    place_barcode*: str - Штрихкод места
    cargo_types: Optional[List[str]] - Типы товаров в заказе. Используйте этот параметр, чтобы обозначить особые требования по обращению с товаром
                        Example: ["80"]
    """
    article: str
    billing_details: ItemBillingDetails
    count: int
    name: str
    place_barcode: str
    cargo_types: Optional[List[str]] = None

class RequestInfo(BaseModel):
    """
    operator_request_id*: str - Идентификатор заказа у отправителя
    comment: str - Комментарий к заказу
    """
    operator_request_id: str
    comment: Optional[str] = None


class PlacePhysicalDimensions(BaseModel):
    """
    placePhysicalDimensions: Весогабаритные характеристики грузомест
    dx*: int - Длина, сантиметры
    dz*: int - Ширина, сантиметры
    dy*: int - Высота, сантиметры
    weight_gross*: int - Вес брутто, граммы
    """
    dx: int
    dz: int
    dy: int
    weight_gross: int


class ResourcePlace(BaseModel):
    """
    resourcePlace: информация о месте
    barcode*: str - Штрихкод места
    physical_dims*: PlacePhysicalDimensions - Физические параметры места 
    description: str - Описание коробки
    """
    barcode: str = Field(default="barcode")
    physical_dims: PlacePhysicalDimensions
    description: Optional[str] = None


class PlatformStation(BaseModel):
    """
    platformStation: информация о платформенной станции
    platform_station_id*: str - ID платформенной станции, зарегистрированной в платформе
    """
    platform_station_id: str


class SourceRequestNode(BaseModel):
    """
    Класс для указания точки отправления заказа
    platform_station_id: str - ID склада отправки, зарегистрированного в платформе
    interval_utc: TimeIntervalUTC - Временной интервал забора заказа со склада отправки в формате UTC
    """
    platform_station: PlatformStation
    interval_utc: TimeIntervalUTC