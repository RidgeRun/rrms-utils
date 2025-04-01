#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Display JSON configuration model
"""
from typing import List

from pydantic import BaseModel


class CameraInputs(BaseModel):
    """Stream URIs of the cameras
    """
    cameras: List[str]


class DisplayConfiguration(BaseModel):
    """Display configuration model
    """
    inputs: CameraInputs
    heatmap: bool
