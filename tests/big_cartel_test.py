from big_cartel.big_cartel import BigCartel


def test_get_account_info():
    bcc = BigCartel()
    account_info = bcc.get_account_info()
    print(account_info.data.id)

    assert 1!=1

def test_get_orders():
    bcc = BigCartel()
    orders = bcc.get_orders(limit=20)
    print(orders)
    for i, order in enumerate(orders):
        print(i, order)
    assert 1==1
