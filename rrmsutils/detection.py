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
Wrapper for Detection API
"""
import requests

from rrmsutils.models.detection.search import Search
from rrmsutils.models.detection.source import Source

__all__ = ['Detection']


class Detection():
    """
    Wrapper for Detection API
    """
    __headers_get = {"Accept": "application/json"}

    def __init__(self, host="127.0.0.1", port=5030, base_path="") -> None:
        """Clien for PTZ service

        Args:
            host (str, optional): Detection server address. Defaults to "127.0.0.1".
            port (int, optional): Detection server port. Defaults to 5030.
        """
        if base_path:
            base_path = f'/{base_path.strip("/")}'
        self.__base = f'http://{host}:{port}{base_path}'
        self.__search = self.__base + '/search'
        self.__source = self.__base + '/source'

    def __get(self, url: str, params):
        return requests.get(url, headers=self.__headers_get, params=params, timeout=100)

    def __put(self, url: str, params: str):
        return requests.put(url, params=params, timeout=100)

    def search_objects(self, search: Search) -> bool:
        """
        Search for given objects and thresholds

        Args:
           search (Search): Search configuration

        Returns:
           bool: True in case of success, False in case of error
        """
        try:
            data = Search.model_validate(search)
            params = {
                "objects": ",".join(data.objects),
                "thresholds": ",".join(map(str, data.thresholds))
            }
        except Exception:
            return False

        try:
            response = self.__get(self.__search, params)
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True

    def set_source(self, source: Source) -> bool:
        """
        Sets the Detection source stream from VST

        Args:
            source (Source): The camera stream name

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Source.model_validate(source)
        except Exception:
            return False

        try:
            response = self.__put(self.__source, data)
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True


if __name__ == "__main__":
    detection = Detection(host="192.168.86.30",
                          port=30080, base_path="/detect")

    search_model = Search(objects=["a person", "a dog"], thresholds=[0.2, 0.6])
    detection.search_objects(search_model)

    source_model = Source(name="loop")
    detection.set_source(source_model)
