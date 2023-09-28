import httpx

from src.correos.schema import SearchResponse, PackeageNotFoundException, Shipment


class Correos:

    def __init__(self):
        self._http_client = self._get_http_client()

    def _get_http_client(self):
        return httpx.Client(
            base_url='https://api1.correos.es',
            headers={
                'Accept': 'application/json'
            }
        )

    def get_package_status(self, package_reference: str) -> SearchResponse:
        params = {
            'text': package_reference,
            'language': "ES",
            'searchType': 'envio'
        }
        response = self._http_client.get('/digital-services/searchengines/api/v1/', params=params)
        match response.status_code:
            case 200:
                return SearchResponse(**response.json()).shipment
            case 404:
                raise PackeageNotFoundException("Package not found")
            case _:
                raise Exception(f"error with request {response.status_code}: {response.text}")

    def get_last_known_status(self, shipment: Shipment):
        if len(shipment.events) == 0:
            return None
        else:
            return sorted(shipment.events, key=lambda x: x.eventDate, reverse=True)[0]
