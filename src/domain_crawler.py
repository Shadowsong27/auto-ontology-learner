import logging
import requests
import random
import urllib3

from queue import Queue
from bs4 import BeautifulSoup


class SimpleRecursiveDomainCrawler:

    def __init__(self, home_domain):
        self.collision_set = set()
        self.tasks_queue = Queue()
        self.home_domain = home_domain

    def crawl(self, given_url):
        logging.info("connecting to target ...")
        # connect to home domain
        headers = {
            'User-Agent': self.get_random_agent(),
        }
        try:
            resp = requests.get(given_url, headers=headers)
        except urllib3.exceptions.ProtocolError:
            self.crawl_next()
            return

        if resp.status_code == 200:
            logging.info("succesfully connected, building soup")
            soup = BeautifulSoup(resp.content, 'lxml')
        else:
            logging.error("connection failed.")
            self.crawl_next()
            return

        # parse content

        # get all links recursively
        logging.info("parsing for urls ...")
        anchors = soup.find_all("a")
        for anchor in anchors:
            try:
                link = anchor['href']
            except KeyError:
                continue

            if 'http' == link[:4]:
                if link not in self.collision_set:
                    if self.home_domain in link:
                        self.collision_set.add(link)
                        self.tasks_queue.put(link)
        logging.info("parsing completed.")

        if self.tasks_queue.qsize() == 0:
            logging.info("urls exhausted. Process complete.")
            return
        else:
            self.crawl_next()

    def crawl_next(self):
        next_url = self.tasks_queue.get()
        logging.info("next url: {}".format(next_url))
        self.crawl(next_url)

    def get_random_proxy(self):
        # will implemented in the future
        pass

    @staticmethod
    def get_random_agent():
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

    def get_total_number_urls(self):
        logging.info("total_number is {}".format(len(self.collision_set)))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    c = SimpleRecursiveDomainCrawler("https://www.eater.com")
    c.crawl("https://www.eater.com/maps/best-new-restaurants-singapore")
    c.get_total_number_urls()
