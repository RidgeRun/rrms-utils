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
This module provides data models for representing points in 2D and 3D space.

Classes:
    Point3D: A model representing a point in a 3D space.
    Point2D: A model representing a point in a 2D space.

Example usage:
::

    from rrmsutils.models.point import Point3D, Point2D

    point_3d = Point3D(x=1, y=2, z=3)
    point_2d = Point2D(x=1, y=2)

    print(point_3d)
    print(point_2d)
"""

from pydantic import BaseModel


class Point3D(BaseModel):
    """
    Model representing a point in a 3D space.

    Attributes:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
        z (int): The z-coordinate of the position. Defaults to 0.
    """

    x: int
    y: int
    z: int = 0


class Point2D(BaseModel):
    """
    Model representing a point in a 2D space.

    Attributes:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
    """

    x: int
    y: int
