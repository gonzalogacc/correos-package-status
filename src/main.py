from datetime import datetime

from big_cartel.big_cartel import BigCartel
from correos.correos import Correos

if __name__ == "__main__":
    bc = BigCartel()
    cr = Correos()
    orders = bc.get_orders(limit=200)

    with open('salida.txt', 'w') as ofile:
        for i, order in enumerate(orders):

            shipment = bc.get_shipment(order['id'])
            if len(shipment['data']) == 0 or shipment['data'][0]['attributes']['carrier'] != 'Correos (ES)':
                continue
            tracking_number = shipment['data'][0]['attributes']['tracking_number']
            # tracking_info = cr.get_last_known_status(cr.get_package_status(tracking_number))
            try:
                tracking_info = cr.get_package_status(tracking_number)[0]
                # outstring = f"{i}, {order['id']}, {tracking_number}, {'|'.join([':'.join([ti.desPhase, ti.eventDate.strftime('%Y-%m-%d')]) for ti in tracking_info.events])}"
                for event in tracking_info.events:
                    outstring=f"{i}, {order['id']}, {tracking_number}, {event.desPhase}, {event.eventDate.strftime('%Y-%m-%d')}"
                    print(outstring)
            except Exception as exc:
                print("Tracking failed", exc)
                outstring = f"{i}, {order['id']}, {tracking_number}, NULL"
                print(outstring)

            ofile.write(f"{outstring}\n")

        ofile.flush()