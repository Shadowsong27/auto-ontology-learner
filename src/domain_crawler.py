import logging
import requests
import random

from bs4 import BeautifulSoup


class DomainCrawler:

    def crawl(self, given_url):
        # connect to home domain
        headers = {
            'User-Agent': self.get_random_agent(),
        }
        resp = requests.get(given_url, headers=headers)
        if resp.status_code == 200:
            logging.info("succesfully connected, building soup")
            soup = BeautifulSoup(resp.content, 'lxml')
        else:
            logging.error("Domain access failed.")
            return

        # get all links recursively
        anchors = soup.find_all("a")
        for anchor in anchors:
            print(anchor['href'])

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    c = DomainCrawler()
    c.crawl("http://www.fratinilatrattoria.com")
