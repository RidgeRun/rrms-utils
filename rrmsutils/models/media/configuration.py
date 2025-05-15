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
Media JSON configuration model
"""

from typing import List, Optional

from pydantic import BaseModel
from rrmsutils.models.point import Point2D


class Resolution(BaseModel):
    """
    Video Resolution
    """
    width: int
    height: int


class Stream(BaseModel):
    """
    Output RTSP stream configuration
    """
    resolution: Optional[Resolution] = Resolution(width=0, height=0)
    brightness: float
    port: int
    mapping: str
    bitrate: int
    uri: Optional[str] = None


class Camera(BaseModel):
    """
    Input camera configuration
    """
    id: str
    index: int


class Configuration(BaseModel):
    """
    Media configuration model
    """
    inputs: List[Camera]
    output: Stream
    cam_position: Point2D
    head_pose_confidence: float
