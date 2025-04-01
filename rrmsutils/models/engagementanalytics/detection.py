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
This module defines the data models for the detection events in the engagement analytics service.

The Detection model represents an individual's detection event, including the object's ID,
the position of the object, and the direction in which the object is moving.

The Frame model represents a single frame with its detections, including the frame ID,
camera ID, timestamp, frame dimensions, and a list of detections.

Example JSON structure for Detection:
{
    "objectid": "object1",
    "position": {
        "x": 10,
        "y": 20,
        "z": 0
    },
    "direction": {
        "x": 1,
        "y": 0,
        "z": -1
    }
}

Example JSON structure for Frame:
{
    "id": 1,
    "cameraid": "camera1",
    "timestamp": "2025-01-01T00:00:00Z",
    "width": 1920,
    "height": 1080,
    "detections": [
        {
            "objectid": "object1",
            "position": {
                "x": 10,
                "y": 20,
                "z": 0
            },
            "direction": {
                "x": 1,
                "y": 0,
                "z": -1
            }
        }
    ]
}
"""

from typing import List

from pydantic import BaseModel

from rrmsutils.models.point import Point3D


class Detection(BaseModel):
    """
    Detection model representing an individual's detection event.

    Attributes:
        objectid (str): Unique identifier for the object detected.
        position (Point3D): The position of the object when detected.
        direction (Point3D): The direction in which the object is moving when detected.
    """

    objectid: str
    position: Point3D
    direction: Point3D


class Frame(BaseModel):
    """
    Frame model representing a single frame with its detections.

    Attributes:
        id (int): Unique identifier for the frame.
        cameraid (str): Unique identifier for the camera that detected the object.
        timestamp (str): Timestamp of when the frame was captured.
        width (int): Width of the frame in pixels.
        height (int): Height of the frame in pixels.
        detections (List[Detection]): List of detections found in the frame.
    """

    id: int
    cameraid: str
    timestamp: str
    width: int
    height: int
    detections: List[Detection]
