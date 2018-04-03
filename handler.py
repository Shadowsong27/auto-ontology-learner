import pymysql

from access_token import LOCAL_DATABASE_ACCESS


class BaseHandler:

    def __init__(self):
        self.conn = pymysql.connect(*LOCAL_DATABASE_ACCESS, charset='utf8')
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()


class PosPatternHandler(BaseHandler):

    def insert_pos_pattern(self, pair):
        try:
            self.cursor.execute(
                """
                INSERT INTO PosDistribution (TagString, Frequency, Type)
                VALUES (%s, %s, %s)
                """, (
                    pair[0],
                    pair[1],
                    pair[2]
                )
            )
        except pymysql.err.IntegrityError:
            pass

    def truncate_pos_dist(self):
        self.cursor.execute(
            """
            TRUNCATE TABLE PosDistribution
            """
        )
        self.conn.commit()

    def get_patterns_above_ratio_for_noun(self, ratio):
        self.cursor.execute(
            """
            SELECT 
              TagString, 
              Frequency / 
                (
                  SELECT MAX(Frequency) FROM PosDistribution
                ) AS ratio
            FROM PosDistribution
            WHERE Type='noun'
            HAVING ratio >= %s ORDER BY ratio DESC
            """, (ratio, )
        )
        return self.cursor.fetchall()

    def get_patterns_above_ratio_for_verb(self, ratio):
        self.cursor.execute(
            """
            SELECT 
              TagString, 
              Frequency / 
                (
                  SELECT MAX(Frequency) FROM PosDistribution
                ) AS ratio
            FROM PosDistribution
            WHERE Type='verb'
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

    def get_domain_id(self, domain_string):
        self.cursor.execute(
            """
            SELECT id FROM Domain
            WHERE DomainUrl=%s
            """, (domain_string, )
        )
        return self.cursor.fetchone()[0]

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

    def insert_domain_body(self, domain_id, hashed_url, body, page_url):
        self.cursor.execute(
            """
            INSERT INTO DomainBody (DomainId, HashedUrl, Body, PageUrl)
            VALUES (%s, %s, %s, %s)
            """, (
                domain_id,
                hashed_url,
                body,
                page_url
            )
        )
        self.commit()


class ParserHandler(BaseHandler):

    def get_domain_bodies_by_id(self, domain_id):
        self.cursor.execute(
            """
            SELECT Body, HashedUrl FROM DomainBody
            WHERE DomainId=%s
            """, (domain_id, )
        )
        return self.cursor.fetchall()

    def get_domain(self, domain_id):
        self.cursor.execute(
            """
            SELECT DomainUrl FROM Domain
            WHERE id=%s
            """, (
                domain_id
            )
        )
        return self.cursor.fetchone()[0]

    def insert_anchor(self, anchor):
        try:
            self.cursor.execute(
                """
                INSERT INTO KnowledgeGraph (SearchType, PrimarySearch, ParsedData)
                VALUES (%s, %s, %s)
                """, (
                    "anchor",
                    anchor.text,
                    anchor.direction
                )
            )
        except pymysql.err.IntegrityError:
            pass

    def insert_short(self, short):
        try:
            self.cursor.execute(
                """
                INSERT INTO KnowledgeGraph (SearchType, PrimarySearch, ParsedData)
                VALUES (%s, %s, %s)
                """, (
                    "short",
                    short.concept_type,
                    short.text
                )
            )
        except pymysql.err.IntegrityError:
            pass

    def insert_long(self, long):
        try:
            self.cursor.execute(
                """
                INSERT INTO KnowledgeGraph (SearchType, PrimarySearch, ParsedData)
                VALUES (%s, %s, %s)
                """, (
                    "long",

                )
            )
        except pymysql.err.IntegrityError:
            pass

