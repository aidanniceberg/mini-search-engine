import json
import logging

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class WebDriver(webdriver.Chrome):
    def parse(self, url: str):
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

        content = None
        description = None
        title = None
        alts = None
        links = None
        h1 = None
        h2 = None
        h3 = None
        h4 = None
        h5 = None
        h6 = None
        paragraphs = None
        linked_data = None
        try:
            content = self._get_content()
            description = self._get_description()
            title = self.title
            alts = self._get_img_alts()
            links = self._get_links()
            h1 = self._agg_text_by_tag("h1")
            h2 = self._agg_text_by_tag("h2")
            h3 = self._agg_text_by_tag("h3")
            h4 = self._agg_text_by_tag("h4")
            h5 = self._agg_text_by_tag("h5")
            h6 = self._agg_text_by_tag("h6")
            paragraphs = self._agg_text_by_tag("p") | self._agg_text_by_tag("div")
            linked_data = self._get_linked_data()
        except StaleElementReferenceException as e:
            logger.error(f"StaleElementReferenceException while parsing {url}: {e}")
        except Exception as e:
            logger.error(f"An unexpected exception occurred: {e}")
            raise e

        logger.info(f"Successfully parsed {url}")

        return (
            dict(
                url=url,
                title=title,
                description=description,
                content=content,
                alts=list(alts) if alts else [],
                h1=list(h1) if h1 else [],
                h2=list(h2) if h2 else [],
                h3=list(h3) if h3 else [],
                h4=list(h4) if h4 else [],
                h5=list(h5) if h5 else [],
                h6=list(h6) if h6 else [],
                paragraphs=list(paragraphs) if paragraphs else [],
                linked_data=linked_data,
            ),
            links if links else [],
        )

    def _get_links(self):
        links = set()
        anchor_tags = self.find_elements(By.TAG_NAME, "a")
        for anchor in anchor_tags:
            href = anchor.get_attribute("href")
            if href is None:
                continue
            parsed = urlparse(href)
            if parsed.scheme not in ("", "http", "https"):
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

    def _agg_text_by_tag(self, tag: str):
        elements = self.find_elements(By.TAG_NAME, tag)
        return set([element.text for element in elements])

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

    def _get_linked_data(self):
        try:
            script_tag = self.find_element(
                By.CSS_SELECTOR, 'script[type="application/ld+json"]'
            )
            html = script_tag.get_attribute("innerHTML")
            return json.loads(html) if html else None
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
