import psycopg2

from habrparser._insertions import InsertProcessor
from habrparser.entities import Article, Author, Group, Article_Group
from habrparser.habrparser import HabrParser


def get_connection(db_name, user, password):
    try:
        conn = psycopg2.connect(dbname=db_name, user=user, password=password)
        return conn
    except psycopg2.Error as e:
        print(e)
        print("Check pass/login/conn")
        input()
        exit(1)


class DatabaseManager:
    """
    Pure fabricated :class:'DatabaseManager' is used for handling SQL 'INSERT' command.

    It is used to
    """

    def __init__(self, db_name, user, password):
        self.__db = get_connection(db_name, user, password)
        self.__insert_p = InsertProcessor(self.get_cursor())

    def add_article(self, link: str):
        parser = HabrParser(link)

        try:
            for group_name in parser.groups:
                self.__insert_group(group_name)

            self.__insert_author(author_name=parser.author)
            self.__insert_article(link=parser.link, title=parser.title,
                                  author_name=parser.author, creation_date=parser.date)

            for group_name in parser.groups:
                self.__connect_article_to_group(parser.title, group_name)

            self.__commit_changes()
            print("Successfully added new article '{article_name}' to database!"
                  .format(article_name=parser.title))
        except psycopg2.Error as e:
            print(e, '\n')

    def __insert_article(self, link: str, title: str, author_name: str, creation_date: str):
        new_article = Article(link, title, author_name, creation_date)
        self.__insert_p.insert_article(new_article)

    def __insert_author(self, author_name: str):
        new_author = Author(author_name)
        self.__insert_p.insert_author(new_author)

    def __insert_group(self, group_name: str):
        new_group = Group(group_name)
        self.__insert_p.insert_group(new_group)

    def __connect_article_to_group(self, article_name: str, group_name: str):
        new_connection = Article_Group(article_name, group_name)
        self.__insert_p.insert_article_group(new_connection)

    def __commit_changes(self):
        self.__db.commit()

    def get_cursor(self):
        return self.__db.cursor()
