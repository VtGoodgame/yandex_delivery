from src import consts as c
import httpx
from schemas.Order_model import (
    BillingInfo,
    PaymentMethod,
    DestinationRequestNode,
    RequestResourceItem,
    ResourcePlace,
    LastMilePolicy,
    ContactPerson,
    SourceRequestNode)


class CreatingOrder():
    """
    Класс для Создание заказа на ближайшее доступное время.
    """
    def __init__(self, api_key: str, base_url: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept-Language": "ru"
        }
        self.base_url = base_url

    async def Creating_an_application(
        self,
        operator_request_id: str,
        source: dict,
        destination: str,
        items: list[dict],
        contact: dict,
        barcode: str):
        """
        Создание заявки
        operator_request_id: str - Идентификатор заказа у отправителя
        source: list[dict] - Список со словарем, содержащим идентификатор ПВЗ-отправителя
        destination: str - Идентификатор ПВЗ-получателя
        items: list[dict] - Список со словарем, содержащим информацию о товаре
        contact: list[dict] - Список со словарем, содержащим информацию о контактном лице
        """
        body = {
            "billing_info": BillingInfo(payment_method=PaymentMethod.already_paid).model_dump(),
            "destination": {
                "type": DestinationRequestNode.platform_station.value,  
                "platform_station_id": destination,
            },
            "info": {"operator_request_id": operator_request_id},
            "items": [
                RequestResourceItem(
                    article=item["article"],
                    billing_details=item["billing_details"],
                    count=item["count"],
                    name=item["name"],
                    place_barcode=item["place_barcode"],
                ).model_dump()
                for item in items
            ],
            "last_mile_policy" : LastMilePolicy.self_pickup.value,
            "places" : [ResourcePlace(
                barcode= barcode,
                physical_dims= item["physical_dims"],
                description= item.get("description")
            ).model_dump()
            for item in items
            ],
            "recipient_info": ContactPerson(
                name=contact["name"],
                phone=contact["phone"],
                email=contact.get("email")
            ).model_dump(),
            "source": SourceRequestNode(
                platform_station=source["platform_station_id"],
                interval_utc=source["interval_utc"]).model_dump(),
            "particular_items_refuse": False
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/request/create", headers=self.headers,params={'send_unix': False}, json=body)
            response.raise_for_status()
            return response.json().get("request_id")