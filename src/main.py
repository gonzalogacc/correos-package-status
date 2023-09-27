from big_cartel.big_cartel import BigCartel

if __name__ == "__main__":
    bc = BigCartel()
    orders = bc.get_orders()
    for order in orders:
        print(order)