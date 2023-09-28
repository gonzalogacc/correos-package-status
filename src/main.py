from big_cartel.big_cartel import BigCartel
from correos.correos import Correos

if __name__ == "__main__":
    bc = BigCartel()
    cr = Correos()
    orders = bc.get_orders(limit=200)
    for i, order in enumerate(orders):
        shipment = bc.get_shipment(order['id'])
        if len(shipment['data']) == 0 or shipment['data'][0]['attributes']['carrier'] != 'Correos (ES)':
            continue
        tracking_number = shipment['data'][0]['attributes']['tracking_number']
        print(i, order['id'], tracking_number, cr.get_last_known_status(cr.get_package_status(tracking_number)[0]))