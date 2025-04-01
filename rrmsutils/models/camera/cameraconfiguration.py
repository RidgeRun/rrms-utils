#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Camera JSON configuration model
"""
from typing import Dict, Optional

from pydantic import BaseModel, RootModel


class Undistort(BaseModel):
    """Undistort configuration parameters
    """
    camera_matrix: str
    distortion_parameters: str
    distortion_model: str


class Resolution(BaseModel):
    """Resolution to capture from a camera
    """
    width: int
    height: int


class Stream(BaseModel):
    """Streaming configuration for a camera
    """
    port: int
    mapping: str
    bitrate: int
    uri: Optional[str] = None


class CameraConfig(BaseModel):
    """Resolution and streaming configuration of a camera
    """
    index: int
    undistort: Undistort
    resolution: Resolution
    streaming: Stream


class CamerasConfiguration(RootModel):
    """Camera configuration model
    """
    root: Dict[str, CameraConfig]

    def __iter__(self):
        return iter(self.root.items())
