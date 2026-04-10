import sys
from pathlib import Path

# Add sources/open_meteo to the path so connector imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sources" / "open_meteo"))

from open_meteo import OpenMeteoLakeflowConnect
from test_suite import LakeflowConnectTests


class TestOpenMeteoConnector(LakeflowConnectTests):
    connector_class = OpenMeteoLakeflowConnect
    sample_records = 5
