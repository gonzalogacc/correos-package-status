from big_cartel.big_cartel import BigCartel


def test_get_account_info():
    bcc = BigCartel()
    account_info = bcc.get_account_info()
    print(account_info.data.id)

    assert 1!=1

def test_get_orders():
    bcc = BigCartel()
    orders = bcc.get_orders(limit=20)
    for i, order in enumerate(orders):
        shipment = bcc.get_shipment(order['id'])
        if len(shipment['data']) == 0 or shipment['data'][0]['attributes']['carrier'] != 'Correos (ES)':
            continue
        print(shipment)
        tracking_number = shipment['data'][0]['attributes']['tracking_number']
        print(i, order['id'], tracking_number)
    assert 1==1
