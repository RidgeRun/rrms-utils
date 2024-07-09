"""
 Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
 All Rights Reserved.

 The contents of this software are proprietary and confidential to RidgeRun,
 LLC.  No part of this program may be photocopied, reproduced or translated
 into another programming language without prior written consent of
 RidgeRun, LLC.  The user is free to modify the source code after obtaining
 a software license from RidgeRun.  All source code changes must be provided
 back to RidgeRun without any encumbrance.
"""
from pydantic import BaseModel


class ServiceConfiguration(BaseModel):
    """
    Configuration of service to move the camera
    """
    enable: bool
    port: int
    ip: str
    time_threshold: int

class Configuration(BaseModel):
    """ Services configuration """
    move_camera: ServiceConfiguration
    record: ServiceConfiguration
