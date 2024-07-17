from flask import Blueprint

from projects.engine.endpoints.v1.search import SearchAPI


class V1App(Blueprint):
    def __init__(self):
        super().__init__("V1App", __name__)

        self.register_blueprint(SearchAPI(), url_prefix="/search")
