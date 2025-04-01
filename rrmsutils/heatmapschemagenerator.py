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
This module provides the `HeatmapSchemaGenerator` class, which is used to generate and manage heatmap schemas,
and interact with a Redis stream for storing and retrieving heatmap data.

Example usage:
::

    from rrmsutils.heatmapschemagenerator import HeatmapSchemaGenerator
    from rrmsutils.models.heatmap import Blob, Heatmap
    from rrmsutils.models.point import Point2D

    generator = HeatmapSchemaGenerator("heatmap")
    heatmap = Heatmap(
        heatmap=[
            Blob(
                position=Point2D(x=1, y=2),
                intensity=0.5,
                radius=20
            ),
            Blob(
                position=Point2D(x=3, y=4),
                intensity=0.45,
                radius=10
            ),
            Blob(
                position=Point2D(x=5, y=6),
                intensity=0.51,
                radius=40
            ),
            Blob(
                position=Point2D(x=7, y=8),
                intensity=0.65,
                radius=25
            )
        ]
    )
    generator.send(heatmap)
    data, _ = generator.get()
    print(data)
"""

from typing import Tuple

from rrmsutils.models.heatmap import Heatmap
from rrmsutils.utils.redisclient import RedisClient


class HeatmapSchemaGenerator():
    """
    A class to generate and manage heatmap schemas, and interact with a Redis stream.
    """

    def __init__(self, redis_stream: str, redis_port: int = 6379, redis_host: str = "localhost"):
        """
        Initializes the HeatmapSchemaGenerator with the specified Redis stream, port, and host.

        Args:
            redis_stream (str): The name of the Redis stream to connect to.
            redis_port (int, optional): The port number of the Redis server. Defaults to 6379.
            redis_host (str, optional): The hostname of the Redis server. Defaults to "localhost".
        """

        self.__redis_stream = redis_stream
        self.__redis_port = redis_port
        self.__redis_host = redis_host

        self.__redis = RedisClient(self.__redis_host, self.__redis_port)

    def send(self, heatmap: Heatmap) -> bool:
        """
        Sends a heatmap to a Redis stream.

        Args:
            heatmap (Heatmap): The heatmap object to be sent.
        Returns:
            bool: True if the heatmap was successfully written to the Redis stream, False otherwise.
        """

        try:
            Heatmap.model_validate(heatmap)
        except Exception as e:
            print(f"Error validating data: {e}")
            return False

        heatmap_str = heatmap.model_dump_json()

        return self.__redis.write_to_stream(self.__redis_stream, {"data": heatmap_str})

    def get(self, block: int = 5000, last_id='$') -> Tuple[Heatmap, str]:
        """
        Retrieves a heatmap from the Redis stream.

        Args:
            block (int, optional): The maximum amount of time (in milliseconds) to block while waiting for data. Defaults to 5000.
            last_id (str, optional): The ID of the last processed entry in the stream. Defaults to '$', which means the latest entry.
        Returns:
            Tuple[Heatmap, str]: A tuple containing the Heatmap object and the ID of the last processed entry.
                                 If no heatmap is retrieved, returns (None, last_id).
        """

        heatmap, last_id = self.__redis.read_from_stream(
            stream=self.__redis_stream, count=1, block=block, last_id=last_id)

        if not heatmap or len(heatmap) == 0:
            return None, last_id

        _, data = heatmap[0][1][0]

        heatmap = None
        try:
            heatmap = Heatmap.model_validate_json(data['data'])
        except Exception as e:
            print(f"Error reading from stream {self.__redis_stream}: {e}")
            return None, last_id

        return heatmap, last_id
