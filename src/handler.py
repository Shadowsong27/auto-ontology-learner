import pymysql

from src.access_token import LOCAL_DATABASE_ACCESS


class BaseHandler:

    def __init__(self):
        self.conn = pymysql.connect(*LOCAL_DATABASE_ACCESS)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()


class PosPatternHandler(BaseHandler):

    def insert_pos_pattern(self, pair):
        self.cursor.execute(
            """
            INSERT INTO PosDistribution (TagString, Frequency)
            VALUES (%s, %s)
            """, (
                pair[0],
                pair[1]
            )
        )

    def truncate_pos_dist(self):
        self.cursor.execute(
            """
            TRUNCATE TABLE PosDistribution
            """
        )
        self.conn.commit()

    def get_patterns_above_ratio(self, ratio):
        self.cursor.execute(
            """
            SELECT 
              TagString, 
              Frequency / 
                (
                  SELECT MAX(Frequency) FROM PosDistribution
                ) AS ratio
            FROM PosDistribution
            HAVING ratio >= %s ORDER BY ratio DESC
            """, (ratio, )
        )
        return self.cursor.fetchall()


class CrawlerHandler(BaseHandler):

    def check_domain_crawled(self, domain_string):
        self.cursor.execute(
            """
            SELECT Status FROM Domain
            WHERE DomainUrl=%s
            """, (domain_string, )
        )
        return self.cursor.fetchone()

    def insert_domain(self, domain_string):
        self.cursor.execute(
            """
            INSERT INTO Domain (DomainUrl)
            VALUES (%s)
            """, (domain_string, )
        )
        self.commit()

    def mark_crawled(self, domain_string):
        self.cursor.execute(
            """
            UPDATE Domain SET Status=1
            WHERE DomainUrl=%s
            """, (domain_string, )
        )
        self.commit()
