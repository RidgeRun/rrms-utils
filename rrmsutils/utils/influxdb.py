#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""
This module provides a utility class for interacting with an InfluxDB instance.

The InfluxDB class includes methods for writing data points to an InfluxDB bucket,
querying data from InfluxDB, and managing the connection to the InfluxDB client.

Environment Variable:
    INFLUXDB_TOKEN: The token used for authenticating with the InfluxDB instance. This environment variable must be set.

Example usage:
::

    # InfluxDB Configuration
    my_bucket = "jetson_metrics"
    my_org = "Ridgerun"
    my_url = "http://localhost:8086"

    # Initialize InfluxDB client
    influx_client = InfluxDB(url=my_url, org=my_org, bucket=my_bucket)

    # Example data to write
    my_measurement = "my_metrics"
    my_tags = {"metric_id": "summary"}
    my_fields = {
        "field1": 100,
        "field2": 5,
        "field3": 50,
        "field4": 345
    }

    # Write data to InfluxDB
    if influx_client.write_data(my_measurement, my_tags, my_fields):
        print("Data written to InfluxDB successfully.")
    else:
        print("Failed to write data to InfluxDB.")

    # Query data from InfluxDB
    my_query = f'''
    from(bucket: "{my_bucket}")
    |> range(start: 0)
    |> filter(fn: (r) => r["_measurement"] == "{my_measurement}" and r["metric_id"] == "summary")
    |> last()
    '''
    my_result = influx_client.query_data(my_query)
    for table in my_result:
        for record in table.records:
            print(f"{record.get_field()}: {record.get_value()}")

    # Close the client
    influx_client.close()
"""

import logging
import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDB:
    """
    A class to interact with an InfluxDB instance.

    Attributes:
    -----------
    client : InfluxDBClient
        The client instance to interact with InfluxDB.
    write_api : WriteApi
        The API instance to write data to InfluxDB.
    bucket : str
        The bucket name where data will be written.
    logger : logging.Logger
        The logger instance to log messages.
    """

    def __init__(self, url, org, bucket, logger=None):
        """
        Initializes the InfluxDB client with the provided URL, organization, and bucket.

        Args:
            url (str): The URL of the InfluxDB instance.
            org (str): The organization name in InfluxDB.
            bucket (str): The bucket name in InfluxDB.
            logger (logging.Logger, optional): The logger instance to log messages. Defaults to None.
        Raises:
            ValueError: If the environment variable 'INFLUXDB_TOKEN' is not set.
        """

        token = os.getenv('INFLUXDB_TOKEN')
        if not token:
            raise ValueError("Environment variable INFLUXDB_TOKEN is not set")
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        self.logger = logger or logging.getLogger(__name__)

    def write_data(self, measurement, tags, fields):
        """
        Write data to an InfluxDB bucket.

        This method creates a data point with the specified measurement, tags, and fields,
        and writes it to the InfluxDB bucket associated with this instance.

        Args:
            measurement (str): The name of the measurement.
            tags (dict): A dictionary of tag key-value pairs.
            fields (dict): A dictionary of field key-value pairs.
        Returns:
            bool: True if the data was written successfully, False otherwise.
        """
        try:
            point = Point(measurement)
            for tag_key, tag_value in tags.items():
                point = point.tag(tag_key, tag_value)
            for field_key, field_value in fields.items():
                point = point.field(field_key, field_value)
            self.write_api.write(bucket=self.bucket,
                                 org=self.client.org, record=point)
            return True
        except Exception as e:
            self.logger.error("Error writing data to InfluxDB: %s", e)
            return False

    def query_data(self, query):
        """
        Executes a query against the InfluxDB and returns the result.

        Args:
            query (str): The query string to be executed.
        Returns:
            result: The result of the query execution.
        """

        result = self.client.query_api().query(org=self.client.org, query=query)
        return result

    def close(self):
        """
        Closes the connection to the InfluxDB client.
        This method ensures that the connection to the InfluxDB client is properly closed,
        releasing any resources that were allocated for the connection.
        """

        self.client.close()

    def __del__(self):
        """
        Destructor method that ensures the proper closing of resources.
        This method is called when the object is about to be destroyed. It calls the `close` method to release any resources
        or perform any necessary cleanup.
        """

        self.close()
