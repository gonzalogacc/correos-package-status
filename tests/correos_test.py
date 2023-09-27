import pytest

from src.correos.schema import PackeageNotFoundException
from src.correos.correos import Correos

def test_package_status():
    cc = Correos()
    response = cc.get_package_status("RF285090588ES")
    print(cc.get_last_known_status(response[0]).desPhase)
    assert response[0].shipmentCode == "RF285090588ES"


def test_package_not_found():
    cc = Correos()
    with pytest.raises(PackeageNotFoundException) as exc:
        response = cc.get_package_status("RF285090589ES")
