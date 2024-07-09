#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""
Wrapper for Analytics API
"""
import requests

from rrmsutils.models.analytics.configuration import Configuration

__all__ = ['Analytics']


class Analytics():
    """
    Wrapper for Analytics API
    """
    __headers_get = {"Accept": "application/json"}
    __headers_put = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5020, base_path="") -> None:
        """Client for Analytics service

        Args:
            host (str, optional): Analytics server address. Defaults to "127.0.0.1".
            port (int, optional): Analytics server port. Defaults to 5020.
        """

        if base_path:
            base_path = f'/{base_path.strip("/")}'
        self.__base = f'http://{host}:{port}{base_path}'
        self.__configuration = self.__base + '/configuration'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __put(self, url: str, data: str):
        return requests.put(url, headers=self.__headers_put, data=data, timeout=100)

    def get_configuration(self):
        """Gets the Analytics configuration

        Returns:
            Configuration: The configuration of the analytics service
        """
        try:
            response = self.__get(self.__configuration)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        config = None
        try:
            config = Configuration.model_validate(json_data)
        except Exception:
            return None

        return config

    def set_configuration(self, config: Configuration) -> bool:
        """Sets the configuration to analytics service

        Args:
            Configuration: The analytics service configuration

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Configuration.model_validate(config)
        except Exception:
            return False

        try:
            response = self.__put(self.__configuration, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True


if __name__ == "__main__":
    analytics = Analytics(host="192.168.86.30",
                          port=30080, base_path="/analytics")
    configuration = Configuration(move_camera={"enable": True, "port": 5020, "ip": "127.0.0.1", "time_threshold": 10},
                                  record={"enable": False, "port": 81, "ip": "127.0.0.1", "time_threshold": 10})
    analytics.set_configuration(configuration)
    configuration = analytics.get_configuration()
    print(configuration)
