#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""Wrapper for Engagement Analytics API
"""

import requests

from rrmsutils.models.engagementanalytics.configuration import Configuration

__all__ = ['EngagementAnalytics']


class EngagementAnalytics():
    """Wrapper for Engagement Analytics API
    """

    __headers_get = {"Accept": "application/json"}
    __headers_put = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5053) -> None:
        """Client for Engagement Analytics service

        Args:
            host (str, optional): Engagement Analytics server address. Defaults to "127.0.0.1".
            port (int, optional): Engagement Analytics server port. Defaults to 5053.
        """
        self.__base = f'http://{host}:{port}'
        self.__configuration = self.__base + '/configuration'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __put(self, url: str, data: str):
        return requests.put(url, headers=self.__headers_put, data=data, timeout=100)

    def get_configuration(self):
        """Gets the Engagement Analytics Configuration

        Returns:
            configuration (Configuration): The configuration of the Engagement Analytics service
             or  None in case of error.
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
            configuration = Configuration.model_validate(json_data)
        except Exception:
            return None

        return configuration

    def set_configuration(self, configuration: Configuration) -> bool:
        """Sets the Engagement Analytics configuration

        Args:
            configuration (Configuration): The service configuration

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Configuration.model_validate(configuration)
        except Exception:
            return False

        try:
            response = self.__put(self.__configuration, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True
