import logging

from flask import Flask

from src.consumers.consumer_task import ConsumerTask
from src.endpoints.v1.v1_app import V1App
from src.handlers import RewardHandler


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_blueprint(V1App(), url_prefix="/v1")

        for r in self.url_map.iter_rules():
            self.logger.debug(f"{r.rule} {r.methods}")


log_fmt = (
    "%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s:%(lineno)3s] %(message)s"
)
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

app = FlaskApp(__name__)

if __name__ == "__main__":
    consumer_task = ConsumerTask(channel="new-reward", handler=RewardHandler())
    consumer_task.start()
    app.run(host="0.0.0.0", port=5001)
