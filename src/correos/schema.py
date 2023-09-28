from datetime import datetime, date
from typing import List, Optional, Annotated

from pydantic import BaseModel, BeforeValidator


def parse_date(value: str) -> date:
    return datetime.strptime(
        value,
        "%d/%m/%Y"
    ).date()


ToDate = Annotated[date, BeforeValidator(parse_date)]


class Event(BaseModel):
    eventDate: ToDate
    eventTime: str
    phase: Optional[str] = None
    desPhase: Optional[str] = None
    colour: str
    summaryText: Optional[str] = None
    extendedText: Optional[str] = None
    actionWeb: str
    actionWebParam: str
    codired: str
    emisiones: Optional[str] = None


class Error(BaseModel):
    errorCode: str
    errorDesc: str


class Shipment(BaseModel):
    shipmentCode: str
    events: List[Event]
    date_delivery_sum: Optional[str] = None
    associatedShipments: List[str]
    error: Error
    expeditionCode: Optional[str]
    packagesTotal: Optional[str]
    packageNumber: Optional[str]
    num_order: Optional[str]


class SearchResponse(BaseModel):
    type: str
    expedition: Optional[str] = None
    shipment: List[Shipment]


class PackeageNotFoundException(Exception):
    pass
