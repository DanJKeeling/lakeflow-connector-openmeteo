from databricks.labs.community_connector.sources.open_meteo.open_meteo import OpenMeteoLakeflowConnect
from tests.test_suite import LakeflowConnectTests


class TestOpenMeteoConnector(LakeflowConnectTests):
    connector_class = OpenMeteoLakeflowConnect
    sample_records = 5
