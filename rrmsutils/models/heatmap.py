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
This module provides data models for representing heatmaps.

Classes:
    Blob: A model representing a heatmap spot (or blob) with a specific position,
    intensity, and radius.
    Heatmap: A model representing a heatmap data structure.

Example usage:
::

    from rrmsutils.models.heatmap import Blob, Heatmap
    from rrmsutils.models.point import Point2D

    blob = Blob(position=Point2D(x=10, y=20), intensity=0.8, radius=5.0)
    heatmap = Heatmap(heatmap=[blob])

    print(blob)
    print(heatmap)
"""

from typing import List

from pydantic import BaseModel

from rrmsutils.models.point import Point2D


class Blob(BaseModel):
    """
    Blob represents a heatmap spot (or blob) with a specific position, intensity, and radius.

    Attributes:
        position (Point2D): The 2D coordinates of the blob in the heatmap.
        intensity (float): The intensity value of the blob.
        radius (float): The radius of the blob.
    """

    position: Point2D
    intensity: float
    radius: float


class Heatmap(BaseModel):
    """
    Heatmap model representing a heatmap data structure.

    Attributes:
        heatmap (List[Blob]): A list of Blob objects representing the heatmap data.
    """

    heatmap: List[Blob]
