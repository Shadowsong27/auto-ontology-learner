class QueryTransformer:
    """

    This handles the search interface of the demo application.
    It will use thesaurus.

    """

    def __init__(self):
        pass

    def convert(self, search_string, domain_id):
        search_tokens = search_string.split(" ")
        sql_list = []
        for token in search_tokens:

            like_statement = 'PrimarySearch like \'%{}%\' OR SecondarySearch like \'%{}%\' OR TertiarySearch like \'%{}%\''.format(
                token, token, token
            )

            partial_sql = """
                (SELECT SearchType, PrimarySearch, SecondarySearch, TertiarySearch,
                ParsedData, OriginalContent
                FROM KnowledgeGraph
                WHERE DomainID={} AND """.format(domain_id) + like_statement + ")"
            sql_list.append(partial_sql)

        sql = "\nUNION\n".join(sql_list)
        return sql


if __name__ == '__main__':
    QueryTransformer().convert("chicken food", 1)
