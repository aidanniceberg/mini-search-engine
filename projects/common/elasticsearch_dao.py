from elasticsearch import Elasticsearch


class ElasticsearchDAO:
    conversions = {
        "b": 0,
        "kb": 1,
        "mb": 2,
        "gb": 3,
    }

    def __init__(self, index: str):
        self.index = index

    def search(
        self, client: Elasticsearch, query: str, page: int = 1, page_size: int = 10
    ):
        filters = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^11", "description^10", "h1^9", "h2^8", "h3^7", "h4^6", "h5^5", "h6^4", "paragraphs^3", "content^2", "alts"],
                    "type": "best_fields",
                    "operator": "or",
                    "fuzziness": "AUTO",
                    "prefix_length": 2,
                    "max_expansions": 50
                }
            }
        }
        result = self.fetch(
            client=client, query=filters, page=page, page_size=page_size
        )
        return result.body

    def fetch(
        self, client: Elasticsearch, query: dict, page: int = 1, page_size: int = 10
    ):
        return client.search(index=self.index, body=query, from_=page, size=page_size)

    def insert(self, client: Elasticsearch, id: str | None, body: dict):
        if id:
            return client.index(index=self.index, id=id, body=body)
        return client.index(index=self.index, body=body)

    def upsert(self, client: Elasticsearch, id: str, body: dict):
        entity_exists = client.exists(index=self.index, id=id)
        op = "create" if not entity_exists else "index"
        return client.index(index=self.index, id=id, body=body, op_type=op)

    def get_size(self, client: Elasticsearch, unit: str = "mb"):
        size_b = client.indices.stats(index=self.index)["indices"][self.index][
            "primaries"
        ]["store"]["size_in_bytes"]
        factor = 1024 ** self.conversions.get(unit, 0)
        return size_b / factor
