import logging
from queue import Queue

from projects.common.db import DBController
from projects.common.elasticsearch_dao import ElasticsearchDAO
from projects.common.models.website import WEBSITE_MAPPING
from webdriver_controller import WebDriverController

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self):
        self.dao = ElasticsearchDAO(index="web")

    @staticmethod
    def _create_index():
        with DBController.client() as client:
            if not client.indices.exists(index="web"):
                client.indices.create(index="web", body=WEBSITE_MAPPING)
                logger.info(f"Created index 'web' with mappings")
            else:
                client.indices.put_mapping(index="web", body=WEBSITE_MAPPING)
                logger.info(f"Index 'web' already exists'")

    def crawl(self, start_url: str):
        """
        Begin crawling websites for metadata
        :param start_url: url to start from
        :return:
        """
        self._create_index()

        queue = Queue()
        queue.put(start_url)
        visited = set()

        size_mb = 0

        with WebDriverController.driver() as driver:
            while not queue.empty() and size_mb < 50:
                content, links = driver.parse(url=queue.get())
                if content is None:
                    continue
                with DBController.client() as client:
                    self.dao.upsert(client=client, id=content["url"], body=content)
                    size_mb = self.dao.get_size(client=client)
                for link in links:
                    if link not in visited and link not in queue.queue:
                        queue.put(link)
            print(size_mb)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    crawler = Crawler()
    crawler.crawl(start_url="https://www.bbc.com")
