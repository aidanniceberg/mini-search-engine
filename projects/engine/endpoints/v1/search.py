from flask import Blueprint, g, jsonify, request
from urllib.parse import unquote

from projects.engine.services import SearchService


class SearchAPI(Blueprint):
    def __init__(self):
        super().__init__("search", __name__)
        self.search_service = SearchService()

        self.add_url_rule("/", methods=["GET"], view_func=self.search)

    def search(self):
        query = request.args.get("query")
        page = request.args.get("page", type=int, default=1)
        page_size = request.args.get("size", type=int, default=10)
        if query is None:
            return "No query provided", 400
        query = unquote(query)
        results = self.search_service.search(query=query, page=page, page_size=page_size)
        return jsonify(results)
