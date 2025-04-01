#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Wrapper for Camera API
"""

import requests

from rrmsutils.models.camera.cameraconfiguration import CamerasConfiguration

__all__ = ['Camera']


class Camera():
    """Wrapper for Camera API
    """

    __headers_get = {"Accept": "application/json"}
    __headers_put = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5050) -> None:
        """Client for Camera service

        Args:
            host (str, optional): Camera server address. Defaults to "127.0.0.1".
            port (int, optional): Camera server port. Defaults to 5050.
        """
        self.__base = f'http://{host}:{port}'
        self.__configuration = self.__base + '/configuration'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __put(self, url: str, data: str):
        return requests.put(url, headers=self.__headers_put, data=data, timeout=100)

    def get_configuration(self):
        """Gets the cameras configuration

        Returns:
            CamerasConfiguration or None: The cameras index, resolution
            and streaming configuration. None in case of error
        """
        try:
            response = self.__get(self.__configuration)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        configuration = None
        try:
            configuration = CamerasConfiguration.model_validate(json_data)
        except Exception:
            return None

        return configuration

    def set_configuration(self, configuration: CamerasConfiguration) -> bool:
        """Sets the cameras configuration

        Args:
            configuration (CamerasConfiguration): The cameras configuration

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = CamerasConfiguration.model_validate(configuration)
        except Exception:
            return False

        try:
            response = self.__put(self.__configuration, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True
