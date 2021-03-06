import logging
import random
import requests
import urllib3

from bs4 import BeautifulSoup
from hashlib import blake2b
from queue import Queue
from src.common.handler import CrawlerHandler


class DomainCrawler:

    """
    This class handles the downloading of body text from a given domain.

    It is a simple, naive implementation for prototyping purpose.

    The outcome of running this crawler should save every HTML pages in database with the given
    input of URL
    """

    def __init__(self, given_url):
        logging.info("Initialise crawler")
        self.collision_set = set()
        self.tasks_queue = Queue()
        self.given_url = given_url
        self.home_domain = self._get_domain_from_url(given_url)
        self.handler = CrawlerHandler()

    def execute(self):
        logging.info("Check domain status")
        domain_check_resp = self.handler.check_domain_crawled(self.home_domain)

        if domain_check_resp is None:
            logging.info("Current domain is new, stored and proceed to crawling")
            self.handler.insert_domain(self.home_domain)
            self._crawl()
        else:
            domain_check_resp = domain_check_resp[0]
            if domain_check_resp == 0:
                logging.info("Current domain is found in DB, but not processed")
                self._crawl()
            else:
                logging.info("Current domain has been crawled, exit.")

    def _crawl(self):
        self.collision_set.add(self.home_domain)  # start from home domain
        self.tasks_queue.put(self.home_domain)

        while self.tasks_queue.qsize() > 0:
            self._crawl_each()

        self.handler.mark_crawled(self.home_domain)
        logging.info("Total number of URL crawled: {}".format(len(self.collision_set)))

    def _crawl_each(self):
        current_url = self.tasks_queue.get()
        logging.debug("Fetching page source from {}".format(current_url))
        headers = {
            'User-Agent': self._get_random_agent(),
        }

        try:
            resp = requests.get(current_url, headers=headers, timeout=30)
        except urllib3.exceptions.ProtocolError:
            return
        except requests.exceptions.Timeout:
            return

        if resp.status_code == 200:
            logging.debug("Successfully connected, fetching source")
            content = resp.content
        else:
            logging.error("Connection failed.")
            return

        logging.debug("Saving page source")
        domain_id = self.handler.get_domain_id(self.home_domain)
        hashed_url = self._get_hashed_url(current_url)
        self.handler.insert_domain_body(domain_id, hashed_url, content, current_url)

        # get all links
        # if links not seen before, it will not be added nor processed
        # if links are not seen before, it will be added to both task queue for
        # processing and to collision set for de - duplication (simple naive)
        logging.debug("Parse for links and push tasks into queue")

        self._parse_tasks(content)

        logging.debug("Check for outstanding tasks in queue")

    def _parse_tasks(self, content):
        soup = BeautifulSoup(content, 'lxml')
        anchors = soup.find_all("a")
        for anchor in anchors:
            try:
                link = anchor['href']
            except KeyError:
                continue

            if 'http' == link[:4]:
                if ".jpg" in link:
                    continue
                if link not in self.collision_set:
                    if self.home_domain in link:
                        self.collision_set.add(link)
                        self.tasks_queue.put(link)

    @staticmethod
    def _get_hashed_url(given_url):
        hasher = blake2b(digest_size=32)
        hasher.update(given_url.encode("utf-8"))
        return hasher.hexdigest()

    @staticmethod
    def _get_random_agent():
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 '
            '(KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
        ]
        return random.choice(user_agents)

    @staticmethod
    def _get_domain_from_url(given_url):
        protocol, link_body = given_url.split("//")
        domain = link_body.split("/")[0]
        return protocol + "//" + domain


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    DomainCrawler("http://www.ladyironchef.com/2012/07/club-street-social/").execute()
