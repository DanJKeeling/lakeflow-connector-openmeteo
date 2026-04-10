# Databricks notebook source
from databricks.labs.community_connector.pipeline import ingest
from databricks.labs.community_connector import register

# Enable the injection of connection options from Unity Catalog connections into connectors
spark.conf.set("spark.databricks.unityCatalog.connectionDfOptionInjection.enabled", "true")

# Connector source name
source_name = "open_meteo"

# =============================================================================
# INGESTION PIPELINE CONFIGURATION
# =============================================================================
pipeline_spec = {
    "connection_name": "<YOUR_CONNECTION_NAME>",
    "objects": [
        {
            "table": {
                "source_table": "hourly_forecast",
            }
        },
        {
            "table": {
                "source_table": "daily_forecast",
            }
        },
    ],
}

# Dynamically import and register the LakeFlow source
register(spark, source_name)

# Ingest the tables specified in the pipeline spec
ingest(spark, pipeline_spec)
