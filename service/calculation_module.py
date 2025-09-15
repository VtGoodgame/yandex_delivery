import httpx
from src import consts as c
from schemas.Order_model import (
    PricingDestinationNode,
    OffersInfoLastMilePolicy,
    PickupStationType,
    BillingInfo,
    PaymentMethod,
    PricingSourceNode,
    DestinationRequestNode,
)

class Calculate():
    """
    Класс для работы с расчетом доставки, стоимости доставки и получения информации о ПВЗ
    """
    def __init__(self, api_key: str, base_url: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.base_url = base_url

    async def calculate_delivery(
        self,
        destination: str,
        source: str,
        total_weight: int,
        tariff: str = "self_pickup",
        payment_method: PaymentMethod = PaymentMethod.already_paid,
    ):
        """
        Предварительный расчет стоимости доставки
        destination: str - ID ПВЗ или постамата, зарегистрированного в платформе, в который нужна доставка
        source: str - ID склада отправки, зарегистрированного в платформе
        total_weight: int - Общий вес заказа в граммах (min_value:1)
        tariff: str - Тариф доставки. Возможные значения: self_pickup - Самовывоз из ПВЗ или постамата
        payment_method: PaymentMethod - Метод оплаты. Возможные значения: already_paid - Оплачено заранее
        """
        body = {
            "destination": PricingDestinationNode(platform_station_id=destination).model_dump(),
            "source": PricingSourceNode(platform_station_id=source).model_dump(),
            "total_weight": total_weight,
            "last_mile_policy": tariff,
            "payment_method": payment_method.value,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/pricing-calculator", headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            return {
                "delivery_days": data.get("delivery_days"),
                "pricing_total": data.get("pricing_total"),
            }


    async def delivery_interval(
        self,
        station_id: str
    ):
        """
        Получение интервалов доставки
        station_id: str - ID склада отгрузки, зарегистрированного в платформе
        """
        params = {
            "station_id": PricingSourceNode(platform_station_id = station_id).model_dump(),
            "last_mile_policy": OffersInfoLastMilePolicy.self_pickup.value,
            "send_unix": False,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/offers/info", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get("offers")


    async def list_of_PVZ(self):
        """
        Получение информации о ПВЗ
        """
        body = {
            "is_not_branded_partner_station": True,
            "is_post_office": False,
            "type": PickupStationType.pickup_point.value,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/pickup-points/list", headers=self.headers, json=body)
            response.raise_for_status()
            return response.json().get("points")


