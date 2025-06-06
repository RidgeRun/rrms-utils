#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.

#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Stream model
"""

from pydantic import BaseModel


class Stream(BaseModel):
    """ Stream Model """
    name: str
    """The Stream Name. It will be used to create the channel to share buffers"""
    uri: str
    """RTSP Stream URI"""
