import psycopg2
from InsertProcessor import InsertProcessor
from entities import Article, Author, Group, Article_Group


def get_connection():
    try:
        conn = psycopg2.connect(dbname="habr_db", user="postgres", password="QWERTY676")
        return conn
    except psycopg2.Error as e:
        print(e)
        print("Check pass/login/conn")
        exit(1)


class DatabaseManager:
    def __init__(self):
        self.__db = get_connection()
        self.__insert_p = InsertProcessor(self.__db)

    def insert_article(self, article: Article):
        self.__insert_p.insert_article(article)

    def insert_author(self, author: Author):
        self.__insert_p.insert_author(author)

    def insert_group(self, group: Group):
        self.__insert_p.insert_group(group)

    def commit(self):
        self.__db.commit()

    def insert_article_data(self, article_group: Article_Group):
        self.__insert_p.insert_article_group(article_group)
