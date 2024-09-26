import redis
import logging
from typing import Optional

from src.utils.errors import RedisConnectionError, RedisConnectionNotAliveError


class RedisConnector:
    """Creates and stores the connection to Redis database."""

    def __init__(self, host: str = "127.0.0.1", port: str = "6379", password: Optional[str] = None):
        """
        Initialization of redis connector.

        Args:
            host: Host on which redis database is working.
            port: Port to which redis database is bound to.
            password: Password to authenticate to redis database.
        """
        self.host = host
        self.port = port
        self.connection = self._create_connection(host, port, password)

    def close(self):
        """Closes the connection to redis database."""
        self.connection.connection_pool.disconnect(inuse_connections=True)

    def is_alive(self):
        """Checks if the connection to redis database is alive."""
        logging.debug(f"Checking if connection to Redis database on {self.host=}, {self.port=} is alive.")
        try:
            self.connection.ping()
        except redis.exceptions.ConnectionError as e:
            logging.exception("Connection to Redis database is not alive.")
            raise RedisConnectionNotAliveError(self.host, self.port) from e
        logging.debug(f"Connection to Redis database is alive.")

    @staticmethod
    def _create_connection(host: str, port: str, password: Optional[str] = None) -> redis.Redis:
        """
        Creates connection to Redis database.

        Args:
            host: Host on which redis database is working.
            port: Port to which redis database is bound to.
            password: Password to authenticate to redis database.

        Returns:
            Connection to Redis database
        """
        logging.info(f"Creating connection to Redis database on {host=}, {port=}.")
        try:
            if password is not None:
                connection = redis.Redis(host=host, port=port, password=password)
            else:
                connection = redis.Redis(host=host, port=port)
            connection.ping()
        except redis.exceptions.ConnectionError as e:
            logging.exception(f"Unable to connect to Redis database.")
            raise RedisConnectionError(host, port) from e
        logging.info(f"Successfully created connection to Redis database.")
        return connection
