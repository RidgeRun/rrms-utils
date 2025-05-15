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
This module provides the `DirectionSchemaGenerator` class, which is used to generate and manage direction schemas for a camera feed,
and interact with a Redis stream for storing and retrieving frame data.

Classes:
    DirectionSchemaGenerator: A class to generate and manage direction schemas for a camera feed.

Example:
::

        from rrmsutils.directionschemagenerator import DirectionSchemaGenerator
        from rrmsutils.models.engagementanalytics.detection import Detection, Point3D

        generator = DirectionSchemaGenerator("detection")

        detections = [
            Detection(
                objectid="0",
                position=Point3D(x=0, y=1),
                direction=Point3D(x=0, y=1)
            ),
            Detection(
                objectid="1",
                position=Point3D(x=0, y=1),
                direction=Point3D(x=0, y=1)
            ),
            Detection(
                objectid="2",
                position=Point3D(x=0, y=1),
                direction=Point3D(x=0, y=1)
            )
        ]
        generator.send(detections)
        data, _ = generator.get()
        if data:
            print(data)
        else:
            print("Timed out reading stream")
"""

from datetime import datetime
from typing import List, Tuple

from rrmsutils.models.engagementanalytics.detection import Detection, Frame
from rrmsutils.utils.redisclient import RedisClient


class DirectionSchemaGenerator():
    """
    A class to generate and manage direction schemas for a camera feed,
    and interact with a Redis stream for storing and retrieving frame data.
    """

    def __init__(self, redis_stream: str, redis_port: int = 6379, redis_host: str = "localhost", camera_id: str = None, resolution: tuple = (0, 0)):
        """
        Initializes the DirectionSchemaGenerator instance.
        Args:
            redis_stream (str): The name of the Redis stream.
            redis_port (int, optional): The port number for the Redis server. Defaults to 6379.
            redis_host (str, optional): The hostname of the Redis server. Defaults to "localhost".
            camera_id (str, optional): The ID of the camera. Defaults to None.
            resolution (tuple, optional): The resolution of the camera as a tuple (width, height). Defaults to (0, 0).
        """

        self.__camera_id = camera_id
        self.__resolution = resolution
        self.__redis_stream = redis_stream
        self.__redis_port = redis_port
        self.__redis_host = redis_host
        self.__frame_counter = 0

        self.__redis = RedisClient(self.__redis_host, self.__redis_port)

    def send(self, detections: List[Detection], frame_id: str = None, timestamp: str = None, maxlen: int = 1000) -> bool:
        """
        Sends detection data to a Redis stream.

        Args:
            detections (List[Detection]): A list of Detection objects to be sent.
            frame_id (str, optional): The frame ID. If not provided, it will use the internal frame counter. Defaults to None.
            timestamp (str, optional): The timestamp of the frame. If not provided, the current time will be used. Defaults to None.
            maxlen (int, optional): The maximum number of entries to keep in the Redis stream.
                                    Older entries will be trimmed approximately if the stream exceeds this length. Defaults to 1000.

        Returns:
            bool: True if the data was successfully written to the Redis stream, False otherwise.
        """

        fid = frame_id
        camera = self.__camera_id
        timestamp_str = timestamp
        if not fid:
            fid = self.__frame_counter
            self.__frame_counter += 1

        if not camera:
            camera = "camera"

        if not timestamp_str:
            now = datetime.now()
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")

        frame = Frame(
            id=fid,
            cameraid=camera,
            timestamp=timestamp_str,
            width=self.__resolution[0],
            height=self.__resolution[1],
            detections=detections
        )

        try:
            Frame.model_validate(frame)
        except Exception as e:
            print(f"Error validating data: {e}")
            return False

        frame_str = frame.model_dump_json()

        return self.__redis.write_to_stream(self.__redis_stream, {"data": frame_str}, maxlen=maxlen)

    def get(self, block: int = 5000, last_id='$') -> Tuple[Frame, str]:
        """
        Retrieves a frame from the Redis stream.
        Args:
            block (int, optional): The maximum amount of time (in milliseconds) to block while waiting for a message. Defaults to 5000.
            last_id (str, optional): The ID of the last message received. Defaults to '$', which means the latest message.
        Returns:
            Tuple[Frame, str]: A tuple containing the retrieved frame and the ID of the last message. If no detection is found, returns (None, last_id).
        """

        detection, last_id = self.__redis.read_from_stream(
            stream=self.__redis_stream, count=1, block=block, last_id=last_id)

        if not detection or len(detection) == 0:
            return None, last_id

        _, data = detection[0][1][0]

        frame = None
        try:
            frame = Frame.model_validate_json(data['data'])
        except Exception as e:
            print(f"Error reading from stream {self.__redis_stream}: {e}")
            return None, last_id

        return frame, last_id
