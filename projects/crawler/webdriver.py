import logging

from selenium import  webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class WebDriver(webdriver.Chrome):
    def run(self, url: str):
        """
        Parse a given website
        :param url: url of website
        :return: tuple of (content, links)
        """
        try:
            self.get(url)
        except TimeoutException as e:
            logger.error(f"TimeoutException while parsing {url}: {e}")
            return None, None
        except WebDriverException as e:
            logger.error(f"WebDriverException while parsing {url}: {e}")
            return None, None

        self._wait_for_load()

        content = self._get_content()
        description = self._get_description()
        title = self.title
        alts = self._get_img_alts()
        links = self._get_links()

        logger.info(f"Successfully parsed {url}")

        return (
            dict(
                url=url,
                title=title,
                description=description,
                content=content,
                alts=list(alts),
            ),
            links,
        )

    def _get_links(self):
        links = set()
        anchor_tags = self.find_elements(By.TAG_NAME, "a")
        for anchor in anchor_tags:
            href = anchor.get_attribute("href")
            if href is None:
                continue
            # take out query parameters
            href = href.lower().split("?")[0]
            if href.endswith("/"):
                href = href[:-1]
            links.add(href)
        return links

    def _get_img_alts(self):
        alts = set()
        img_tags = self.find_elements(By.TAG_NAME, "img")
        for img in img_tags:
            if alt := img.get_attribute("alt"):
                alts.add(alt)
        return alts

    def _get_content(self):
        try:
            body_element = self.find_element(By.TAG_NAME, "body")
            return body_element.text
        except NoSuchElementException:
            return None

    def _get_description(self):
        try:
            description_tag = self.find_element(
                By.CSS_SELECTOR, 'meta[name="description"]'
            )
            return description_tag.get_attribute("content")
        except NoSuchElementException:
            return None

    def _wait_for_load(self):
        """
        Wait for a website's content to load
        :return: true if all conditions load, false if not
        """
        try:
            WebDriverWait(self, 10).until(
                expected_conditions.all_of(
                    lambda driver: driver.execute_script("return document.readyState")
                    == "complete",
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, 'meta[name="description"]')
                    ),
                    expected_conditions.presence_of_element_located(
                        (By.TAG_NAME, "title")
                    ),
                )
            )
        except TimeoutException:
            return False
        except Exception as e:
            logger.error(f"Unexpected error occurred waiting for content to load: {e}")
            raise e
        return True


if __name__ == "__main__":
    parser = Parser()
    print(parser.run(url="https://blog.hubspot.com/marketing/meta-tags"))
