from flask import Blueprint

from src.endpoints.v1.rewards import RewardsAPI


class V1App(Blueprint):
    def __init__(self):
        super().__init__("V1App", __name__)

        self.register_blueprint(RewardsAPI(), url_prefix="/rewards")
