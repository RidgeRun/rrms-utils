#  Copyright (C) 2025 RidgeRun, LLC (http://www.ridgerun.com)
#  All Rights Reserved.
#
#  The contents of this software are proprietary and confidential to RidgeRun,
#  LLC.  No part of this program may be photocopied, reproduced or translated
#  into another programming language without prior written consent of
#  RidgeRun, LLC.  The user is free to modify the source code after obtaining
#  a software license from RidgeRun.  All source code changes must be provided
#  back to RidgeRun without any encumbrance.

"""
This module provides a Redis client utility class for interacting with a Redis server.

The RedisClient class includes methods for setting and getting key-value pairs, setting
and getting dictionaries, incrementing fields, writing to and reading from Redis streams,
and checking if a key exists.

Example usage:
::

    redis_client = RedisClient()
    redis_client.set("key", "value")
    value = redis_client.get("key")
    exists = redis_client.exists("key")
"""

import logging

from redis import Redis


class RedisClient:
    """Redis client
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, logger=None):
        """
        Initializes a new instance of the Redis utility class.

        Args:
            host (str): The hostname of the Redis server. Defaults to 'localhost'.
            port (int): The port number on which the Redis server is listening. Defaults to 6379.
            logger (logging.Logger, optional): The logger instance to log messages. Defaults to None.
        """

        self._redis = Redis(host=host, port=port, decode_responses=True)
        self.logger = logger or logging.getLogger(__name__)

    def set(self, key: str, value: str, ex: int = None) -> bool:
        """Set a key-value pair in Redis with an optional expiration time

        Args:
            key (str): The key to set
            value (str): The value to set
            ex (int, optional): The expiration time in seconds. Defaults to None.

        Returns:
            bool: True if the key was set successfully, False otherwise.
        """
        try:
            self._redis.set(key, value, ex=ex)
            return True
        except Exception as e:
            self.logger.error("Error setting key in Redis: %s", e)
            return False

    def get(self, key: str) -> str:
        """Get the value of a key from Redis

        Args:
            key (str): The key to get

        Returns:
            str: The value of the key
        """
        return self._redis.get(key)

    def delete(self, key: str):
        """Delete a key from Redis

        Args:
            key (str): The key to delete
        """
        self._redis.delete(key)

    def set_dict(self, key: str, value: dict, ex: int = None) -> bool:
        """Set a key with a dictionary of key-value pairs in Redis with an optional expiration time

        Args:
            key (str): The key to set
            value (dict): The dictionary of key-value pairs to set
            ex (int, optional): The expiration time in seconds. Defaults to None.

        Returns:
            bool: True if the dictionary was set successfully, False otherwise.
        """
        try:
            self._redis.hset(key, mapping=value)
            if ex is not None:
                self._redis.expire(key, ex)
            return True
        except Exception as e:
            self.logger.error("Error setting dictionary in Redis: %s", e)
            return False

    def get_dict(self, key: str) -> dict:
        """Get the dictionary of key-value pairs from Redis

        Args:
            key (str): The key to get

        Returns:
            dict: The dictionary of key-value pairs
        """
        return self._redis.hgetall(key)

    def set_field(self, key: str, field: str, value: str, ex: int = None) -> bool:
        """Set a single field of a key in Redis with an optional expiration time

        Args:
            key (str): The key to set the field for
            field (str): The field to set
            value (str): The value to set for the field
            ex (int, optional): The expiration time in seconds. Defaults to None.

        Returns:
            bool: True if the field was set successfully, False otherwise.
        """
        try:
            self._redis.hset(key, field, value)
            if ex is not None:
                self._redis.expire(key, ex)
            return True
        except Exception as e:
            self.logger.error("Error setting field in Redis: %s", e)
            return False

    def increment_field(self, key: str, field: str, value: int, ex: int = None) -> bool:
        """Increment a single field of a key by the given value in Redis with an optional expiration time

        Args:
            key (str): The key to increment the field for
            field (str): The field to increment
            value (int): The value to increment the field by
            ex (int, optional): The expiration time in seconds. Defaults to None.

        Returns:
            bool: True if the field was incremented successfully, False otherwise.
        """
        try:
            self._redis.hincrby(key, field, value)
            if ex is not None:
                self._redis.expire(key, ex)
            return True
        except Exception as e:
            self.logger.error("Error incrementing field in Redis: %s", e)
            return False

    def write_to_stream(self, stream: str, data: dict, maxlen: int = 1000) -> bool:
        """Write data to a Redis stream

        Args:
            stream (str): The name of the stream
            data (dict): The data to write to the stream
            maxlen (int): The maximum number of entries to keep in the stream. Older entries will be trimmed
                          automatically if the stream exceeds this length. The trimming is approximate for performance reasons.
        Returns:
            bool: True if the data was written successfully, False otherwise.
        """
        try:
            self._redis.xadd(stream, data, maxlen=maxlen, approximate=True)
            return True
        except Exception as e:
            self.logger.error("Error writing to stream in Redis: %s", e)
            return False

    def read_from_stream(self, stream: str, count: int = 1, block: int = 0, last_id: str = '0-0') -> tuple:
        """Read data from a Redis stream

        Args:
            stream (str): The name of the stream
            count (int, optional): The number of entries to read. Defaults to 1.
            block (int, optional): The maximum number of milliseconds to block if no entries are available. Defaults to 0.
            last_id (str, optional): The ID to start reading from. Defaults to '0-0'.

        Returns:
            tuple: A tuple containing the list of stream entries and the last read message ID
        """
        try:
            entries = self._redis.xread(
                {stream: last_id}, count=count, block=block)
            if entries:
                last_id = entries[0][1][-1][0]
            return entries, last_id
        except Exception as e:
            self.logger.error("Error reading from stream in Redis: %s", e)
            return [], last_id

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis

        Args:
            key (str): The key to check

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            return self._redis.exists(key) == 1
        except Exception as e:
            self.logger.error("Error checking if key exists in Redis: %s", e)
            return False
