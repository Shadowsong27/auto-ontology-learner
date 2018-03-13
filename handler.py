import pymysql

from access_token import LOCAL_DATABASE_ACCESS


class KeywordHandler:

    def __init__(self):
        self.conn = pymysql.connect(*LOCAL_DATABASE_ACCESS)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

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