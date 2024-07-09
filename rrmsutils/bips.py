#  Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""BIPS Microservice Client API

A thypical use case would be as follows::

    from rrmsutils.bips import BIPS
    from rrmsutils.models.bips.stream import Stream
    from rrmsutils.models.bips.streamlist import StreamList

    # Imports needed for bips consumer
    import numpy as np
    import bips

    # Create BIPS client (by default will talk to address 127.0.0.1 and port 5050)
    bips_service = BIPS()

    # Create the Stream object for the desired stream
    stream = Stream(name='camera1', uri='rtsp://127.0.0.1:5000/stream1')

    ret = bips_service.add_stream(stream)
    if not ret:
        print("Something went wrong")

    # Get Streams List
    stream_list = bips_service.get_stream_list()

    # Create bips consumer
    item = stream_list.streams[0]
    buffer = item.buffer

    size = buffer.size
    channel=item.name
    buffers = item.buffers

    backend = bips.Backends.kShm
    in_order = True

    logger = bips.Logger(bips.LoggerType.kSpd, "consumer.log")
    logger.SetConsoleLevel(bips.Level.kWarning)
    logger.SetLogfileLevel(bips.Level.kTrace)

    consumer = bips.Consumer(backend,channel,buffers,size,in_order,logger)

    num_iterations = 120
    timeout = 6000000

    # Start pulling buffers
    for i in range(num_iterations):
        buffer = consumer.Pull(timeout)

        np_array = np.array(buffer.data, copy=False)
        print(np_array[0])

        consumer.Push(buffer, timeout)

    # Delete stream
    bips_service.delete_stream('camera1')
"""

import requests

from rrmsutils.models.bips.stream import Stream
from rrmsutils.models.bips.streamlist import StreamList

__all__ = ['BIPS']


class BIPS():
    """Clien for PTZ service

        Args:
            host (str, optional): BIPS service address. Defaults to "127.0.0.1".
            port (int, optional): BIPS service port. Defaults to 5050.
    """

    __headers_get = {"Accept": "application/json"}
    __headers_post = {
        "Accept": "application/json",
        "Content-type": "application/json"}

    def __init__(self, host="127.0.0.1", port=5050) -> None:
        self.__base = f'http://{host}:{port}'
        self.__stream = self.__base + '/stream'
        self.__stream_list = self.__base + '/stream_list'

    def __get(self, url: str):
        return requests.get(url, headers=self.__headers_get, timeout=100)

    def __post(self, url: str, data: str):
        return requests.post(url, headers=self.__headers_post, data=data, timeout=100)

    def __delete(self, url: str):
        return requests.delete(url, headers=self.__headers_get, timeout=100)

    def get_stream_list(self):
        """Gets stream list

        Returns:
            StreamList: The list of current streams with its information.
        """
        try:
            response = self.__get(self.__stream_list)
            if response.status_code != 200:
                return None
        except Exception:
            return None

        json_data = response.json()
        stream_list = None
        try:
            stream_list = StreamList.model_validate(json_data)
        except Exception:
            return None

        return stream_list

    def add_stream(self, stream: Stream) -> bool:
        """Adds a stream to the service. The stream consists of a module that captures from
        an RTSP stream and generates a channel to share it with other processes.

        Args:
            stream (rrmsutils.models.bips.stream.Stream): The stream to be added.

        Returns:
            bool: True in case of success, False in case of error
        """

        try:
            data = Stream.model_validate(stream)
        except Exception:
            return False

        try:
            response = self.__post(self.__stream, data.model_dump_json())
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True

    def delete_stream(self, name: str) -> bool:
        """Deletes the given stream

        Args:
            name (str): The name of the stream to be deleted

        Returns:
            bool: True in case of success, False in case of error
        """
        try:
            response = self.__delete(self.__stream + '/' + name)
            if response.status_code != 200:
                return False
        except Exception:
            return False

        return True
