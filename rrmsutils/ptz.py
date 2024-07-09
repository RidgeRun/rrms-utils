#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Wrapper for PTZ API
"""

import requests

from rrmsutils.models.ptz.position import Position
from rrmsutils.models.ptz.stream import Stream
from rrmsutils.models.ptz.zoom import Zoom

__all__ = ['PTZ']


class PTZ():
    """Wrapper for PTZ API
    """

    __headers_get = {"Accept": "application/json"}
    __headers_put = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5020) -> None:
        """Clien for PTZ service

        Args:
            host (str, optional): PTZ server address. Defaults to "127.0.0.1".
            port (int, optional): PTZ server port. Defaults to 5020.
        """
        self.__base = f'http://{host}:{port}'
        self.__position = self.__base + '/position'
        self.__zoom = self.__base + '/zoom'
        self.__stream = self.__base + '/stream'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __put(self, url: str, data: str):
        return requests.put(url, headers=self.__headers_put, data=data, timeout=100)

    def get_position(self):
        """Gets the camera position

        Returns:
            Position: The camera position or None in case of error
        """
        try:
            response = self.__get(self.__position)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        position = None
        try:
            position = Position.model_validate(json_data)
        except Exception:
            return None

        return position

    def set_position(self, position: Position) -> bool:
        """Sets the camera position

        Args:
            position (Position): The camera position

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Position.model_validate(position)
        except Exception:
            return False

        try:
            response = self.__put(self.__position, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True

    def get_zoom(self):
        """Gets the camera zoom

        Returns:
            Zoom: The camera zoom or None in case of error
        """
        try:
            response = self.__get(self.__zoom)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        zoom = None
        try:
            zoom = Zoom.model_validate(json_data)
        except Exception:
            return None

        return zoom

    def set_zoom(self, zoom: Zoom) -> bool:
        """Sets the camera zoom

        Args:
            zoom (Zoom): The camera zoom

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Zoom.model_validate(zoom)
        except Exception:
            return False

        try:
            response = self.__put(self.__zoom, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True

    def get_stream(self):
        """Gets the PTZ stream

        Returns:
            rrmsutils.models.ptz.stream.Stream: The camera stream information or None in case of error
        """
        try:
            response = self.__get(self.__stream)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        stream = None
        try:
            stream = Stream.model_validate(json_data)
        except Exception:
            return None

        return stream

    def set_stream(self, stream: Stream) -> bool:
        """Sets the PTZ stream

        Args:
            stream (rrmsutils.models.ptz.stream.Stream): The camera stream information

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Stream.model_validate(stream)
        except Exception:
            return False

        try:
            response = self.__put(self.__stream, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True
