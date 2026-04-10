from open_meteo import OpenMeteoLakeflowConnect
from test_suite import LakeflowConnectTests


class TestOpenMeteoConnector(LakeflowConnectTests):
    connector_class = OpenMeteoLakeflowConnect
    sample_records = 5
