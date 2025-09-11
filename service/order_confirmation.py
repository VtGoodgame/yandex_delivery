import httpx
from src import consts as c

class OrderConfirmation():
    """
    Класс для работы с подтверждением заказа
    """
    def __init__(self, api_key: str, base_url: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = base_url

    async def confirm_order(
        self,
        offer_id: str
    ):
        """
        Подтверждение заказа
        offer_id: str - Идентификатор предложения маршрутного листа.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/offers/confirm", headers=self.headers, json={"offer_id": offer_id})
            response.raise_for_status()
            return response.json().get("request_id")
        
class GetInfoAboutDraft():
    """
    Класс для получения информации о заявке
    """
    def __init__(self, api_key: str, base_url: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = base_url


    async def get_info_about_draft(
            self,
            request_code: str = None,
            request_id: str = None):
        """
        Получение информации о заявке и ее текущем статусе.
        request_code: str - Идентификатор заказа у отправителя
        request_id: str - Идентификатор заказа в системе Яндекс.Доставки
        """
        params = {}
        if request_code:
            params["request_code"] = request_code
        if request_id:
            params["request_id"] = request_id
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/request/info", headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            order_info = {
                        "info": {
                            key: data.get(key)
                            for key in ("full_items_price", "request", "request_id", "sharing_url")
                        },
                        "request_state": {
                            key: data.get("state", {}).get(key)
                            for key in ("description", "status", "timestamp", "timestamp_utc", "reason")
                        },
                        "self_pickup_node_code": {
                            key: data.get("self_pickup_node_code", {}).get(key)
                            for key in ("code", "type")
                        },
                    }

            return {"order_info": order_info}
        
    async def up_to_date_shipping_information(self,request_id: str):
        """
        Получение актуальной даты и времени доставки. Метод актуален только для заказов в статусе, отличном от DELIVERY_DELIVERED, ERROR или CANCELLED.
        request_id*: str - Идентификатор заказа в системе Яндекс.Доставки
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/request/tracking", headers=self.headers, params={"request_id": request_id})
            response.raise_for_status()
            data = response.json()
            return {'delivery_date': data.get('delivery_date'),
                    'delivery_interval': data.get('delivery_interval')} 
        
    async def get_Delivery_interval(self, request_id: str):
        """
        Получение интервала доставки для заказа. Метод актуален только для заказов в статусе, отличном от DELIVERY_DELIVERED, ERROR или CANCELLED.
        request_id*: str - Идентификатор заказа в системе Яндекс.Доставки
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/request/datetime_options", headers=self.headers, json={"request_id": request_id})
            response.raise_for_status()
            data = response.json()
            return {'interval': data.get('options')}
        
    async def get_history_of_status_changes(self, request_id: str):
        """
        Получение истории изменения статусов заказа.
        request_id*: str - Идентификатор заказа в системе Яндекс.Доставки
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/request/history", headers=self.headers, params={"request_id": request_id})
            response.raise_for_status()
            data = response.json()
            return {'history': data.get('state_history')}