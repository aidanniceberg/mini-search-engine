import logging
from contextlib import contextmanager

from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)


class DBController:
    @staticmethod
    def _generate_connection_string() -> str:
        return "http://localhost:9200/"

    @classmethod
    @contextmanager
    def client(cls) -> Elasticsearch:
        """
        Context manager that creates a new elasticsearch client
        :return: client
        """
        client = None
        try:
            client = Elasticsearch(cls._generate_connection_string())
            yield client
        except Exception:
            raise
        finally:
            if client:
                client.close()
