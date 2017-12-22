from habrparser._insertions import InsertProcessor
from habrparser._queries import *
from habrparser.entities import Article, Author, Group, Article_Group


class DatabaseManager:
    """
    Pure fabricated :class: DatabaseManager class is used for grouping two separate classes :class: InsertProcessor and
    :class: SelectProcessor.
    It is used to
    """

    def __init__(self, connection_with_db):
        self.__db = connection_with_db
        self.__cur = connection_with_db.cursor()
        self.__insert_p = InsertProcessor(self.__db)

    def executeQuery(self, query_function, *args):
        result_list = query_function(self.__cur, *args)
        for result in result_list:
            print(result)

    ################### INSERTIONS BY DEFAULT. DO NOT CHANGE ###############################

    def insert_article(self, link: str, title: str, author_name: str, creation_date: str):
        new_article = Article(link, title, author_name, creation_date)
        self.__insert_p.insert_article(new_article)

    def insert_author(self, author_name: str):
        new_author = Author(author_name)
        self.__insert_p.insert_author(new_author)

    def insert_group(self, group_name: str):
        new_group = Group(group_name)
        self.__insert_p.insert_group(new_group)

    def connect_article_to_group(self, article_name: str, group_name: str):
        new_connection = Article_Group(article_name, group_name)
        self.__insert_p.insert_article_group(new_connection)

    ################### QUERIES PROVIDED BY DEFAULT #########################################

    def get_articles_by_group(self, group_name: str, from_time: str, to_time: str):
        self.executeQuery(get_articles_by_group, group_name, from_time, to_time)

    def get_top_groups(self):
        self.executeQuery(get_top_groups)

    def get_top_users(self):
        self.executeQuery(get_top_users)

    def get_articles_by_week(self):
        self.executeQuery(get_articles_by_week)

    def commit(self):
        self.__db.commit()
