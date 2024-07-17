from unittest import result

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from projects.common.db import DBController
from projects.common.elasticsearch_dao import ElasticsearchDAO
from projects.common.models.search_result import SearchResult, SearchResultItem


class SearchService:
    def __init__(self):
        self.dao = ElasticsearchDAO(index="web")

    @staticmethod
    def _filter_stopwords(query: str):
        nltk.download("stopwords")
        stopwords_list = set(stopwords.words("english"))
        tokens = word_tokenize(query)
        filtered_query = [word for word in tokens if word.lower() not in stopwords_list]
        return " ".join(filtered_query)

    def search(self, query: str, page: int = 1, page_size: int = 10):
        # query = self._filter_stopwords(query)
        with DBController.client() as client:
            results = self.dao.search(
                client=client, query=query, page=page, page_size=page_size
            )
        return SearchResult(
            query=query,
            count=results["hits"]["total"]["value"],
            page=page,
            page_size=page_size,
            items=[
                SearchResultItem(
                    title=item["_source"].get("title"),
                    description=item["_source"].get("description"),
                    url=item["_source"].get("url"),
                    linked_data=item["_source"].get("linked_data"),
                )
                for item in results["hits"]["hits"]
            ],
        )
