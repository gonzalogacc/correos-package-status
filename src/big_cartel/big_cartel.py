import base64
import json
import time
from urllib.parse import urlparse

import httpx
import os

from dotenv import load_dotenv

from big_cartel.schema import BigCartelResponse, BigCartelAccount

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


class BigCartel:
    def __init__(self):
        self._http_client = self._get_http_client()

    def _get_http_client(self):
        creds_string = base64.urlsafe_b64encode(f"{USERNAME}:{PASSWORD}".encode("utf-8")).decode("utf-8")
        return httpx.Client(
            base_url="https://api.bigcartel.com/",
            headers={
                'Authorization': f'Basic {creds_string}',
                'User-Agent': 'test project (gonzalogacc@gmail.com)',
                'Accept': 'application/vnd.api+json',
            }
        )

    def get_account_info(self):
        response = self._http_client.get('/v1/accounts')
        assert response.status_code == 200, "Error getting account"
        response = BigCartelResponse(**response.json())
        assert len(response.data) == 1, "Found more than one account, not valid RN"
        return response.data[0]

    def _get_order_batch(self, link=None):
        params = {"sort": "-created_at"}
        account_id = self.get_account_info().id
        if not link:
            response = self._http_client.get(f'/v1/accounts/{account_id}/orders', params=params)
        else:
            parse_link = urlparse(link)
            response = self._http_client.get(parse_link.path)

        assert response.status_code == 200, f"Cant get orders {response.text}"
        return response.json()

    def get_orders(self, force_query=False, limit=100):

        response = self._get_order_batch()
        orders = response['data']

        while len(orders) < int(response['meta']['count']) and 'links' in response and 'next' in response['links'] and len(orders) < limit:
            print("Recovered %s/%s orders --> %s" % (len(orders), response['meta']['count'], response['links']['next']))
            response = self._get_order_batch(link=response['links']['next'])
            orders.extend(response['data'])
            time.sleep(1)

        print("Recovered %s/%s orders --> N/A" % (len(orders), response['meta']['count']))
        return orders

    def get_shipments(self, order_id: str):
        return None


if __name__ == "__main__":
    bc = BigCartel()
    print(bc.get_orders(limit=20))