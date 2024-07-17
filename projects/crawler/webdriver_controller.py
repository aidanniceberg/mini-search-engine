from contextlib import contextmanager

from projects.crawler.webdriver import WebDriver


class WebDriverController:
    @classmethod
    @contextmanager
    def driver(cls) -> WebDriver:
        driver = WebDriver()
        try:
            yield driver
        finally:
            driver.quit()
