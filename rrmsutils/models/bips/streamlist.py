#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.

#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""StreamList model
"""

from typing import List

from pydantic import BaseModel


class Buffer(BaseModel):
    """ Buffer Model """
    width: int
    """Buffer width"""
    height: int
    """Buffer height"""
    format: str
    """Buffer format"""
    size: int
    """Buffer size"""


class Item(BaseModel):
    """ Item Model """
    name: str
    """Stream (channel) name"""
    uri: str
    """RTSP Stream URI"""
    buffer: Buffer
    """Buffer information"""
    buffers: int
    """Number of buffers used by bips"""


class StreamList(BaseModel):
    """ Stream List Model """
    streams: List[Item]
    """List of streams"""
