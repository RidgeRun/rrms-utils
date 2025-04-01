#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Wrapper for Display API
"""

import requests

from rrmsutils.models.display.displayconfiguration import DisplayConfiguration
from rrmsutils.models.display.heatmap import Heatmap

__all__ = ['Display']


class Display():
    """Wrapper for Display API
    """

    __headers_get = {"Accept": "application/json"}
    __headers_put = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5052) -> None:
        """Client for Display service

        Args:
            host (str, optional): Display server address. Defaults to "127.0.0.1".
            port (int, optional): Display server port. Defaults to 5050.
        """
        self.__base = f'http://{host}:{port}'
        self.__configuration = self.__base + '/configuration'
        self.__heatmap = self.__base + '/heatmap'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __put(self, url: str, data: str):
        return requests.put(url, headers=self.__headers_put, data=data, timeout=100)

    def get_configuration(self):
        """Gets the Display configuration

        Returns:
            DisplayConfiguration or None: The cameras identifiers and
            heatmap value. None in case of error
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
            configuration = DisplayConfiguration.model_validate(json_data)
        except Exception:
            return None

        return configuration

    def set_configuration(self, configuration: DisplayConfiguration) -> bool:
        """Sets the Display configuration

        Args:
            configuration (DisplayConfiguration): The display configuration

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = DisplayConfiguration.model_validate(configuration)
        except Exception:
            return False

        try:
            response = self.__put(self.__configuration, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True

    def get_heatmap(self):
        """Gets the heatmap overlay value

        Returns:
            bool or None: The heatmap boolean value. None in case of error
        """
        try:
            response = self.__get(self.__heatmap)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        heatmap = None
        try:
            heatmap = Heatmap.model_validate(json_data)
        except Exception:
            return None

        return heatmap.heatmap

    def set_heatmap(self, heatmap: bool) -> bool:
        """Sets the heatmap overlay value

        Args:
            configuration (bool): The heatmap boolean value to use

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Heatmap.model_validate({"heatmap": heatmap})
        except Exception:
            return False

        try:
            response = self.__put(self.__heatmap, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True
