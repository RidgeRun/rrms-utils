#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Engagement Analytics configuration model

This module defines the data models for the engagement analytics configuration.

JSON Structure:
::

    {
        "heatmap": {
            "window_seconds": int,
            "eps": int,
            "min_samples": int,
            "update_period": int
        },
        "engagement": [
            {
                "id": str,
                "roi": [
                    {
                        "x": int,
                        "y": int,
                        "z": int
                    },
                    ...
                ]
            },
            ...
        ],
        "db_update_period": int,
        "message_expiration": int
    }
"""
from typing import List

from pydantic import BaseModel

from rrmsutils.models.point import Point3D


class Engagement(BaseModel):
    """Engagement model representing an engagement instance.

    Attributes:
        id (str): Unique identifier for the camera containing the ROI.
        roi (List[Point]): List of points defining the region of interest (ROI) for the given camera.

        BaseModel (pydantic.BaseModel): The base model class from which Engagement inherits.
    """
    id: str
    roi: List[Point3D]


class Heatmap(BaseModel):
    """
    Heatmap model representing a heatmap with a specific resolution.

    Attributes:
        window_seconds (int): The time window in seconds for heatmap clustering detections.
        Defaults to 5.
        eps (int): The maximum distance between two samples for them to be considered
        as in the same neighborhood. Defaults to 50.
        min_samples (int): The number of samples in a neighborhood for a point to be
        considered as a core point. Defaults to 3.
        update_period (int): Period in seconds to refresh the heatmap. Defaults to 30 seconds.
    """

    window_seconds: int = 5
    eps: int = 50
    min_samples: int = 3
    update_period: int = 30


class Configuration(BaseModel):
    """
    Configuration model for engagement analytics

    Attributes:
        heatmap (Heatmap): The heatmap data associated with the configuration.
        engagement (List[Engagement]): A list of engagement data.
        db_update_period (int): The period in seconds for updating the database. Defaults to 5.
        message_expiration (int): The period in seconds for engagement to expire. After this time
        the message will disappear from redis. Defaults to 5.
    """

    heatmap: Heatmap
    engagement: List[Engagement]
    db_update_period: int = 5
    message_expiration: int = 5
