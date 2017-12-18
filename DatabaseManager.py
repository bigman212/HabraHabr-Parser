import psycopg2
from InsertProcessor import InsertProcessor
from SelectProcessor import SelectProcessor
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
        self.__select_p = SelectProcessor(self.__db)

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

    def get_articles_by_group(self, group_name, from_time: str, to_time: str):
        result = self.__select_p.get_articles_by_group(group_name, from_time, to_time)
        print("Articles found by {} and between {} - {}".format(group_name, from_time, to_time))
        for columns in result:
                print("|{:<100}|{}|".format(columns[0], columns[1]))
        print()

    def get_top_groups(self):
        result = self.__select_p.get_top_groups()
        print("Top 10 groups")
        print("|{:<40}|{:^20}|".format("Group name", "Articles count"))
        print('-' * 130)
        for columns in result:
            print("|{:<40}|{:^20}|".format(columns[0], columns[1]))
        print()

    def get_top_users(self):
        result = self.__select_p.get_top_users()
        print("Top 10 users")
        print("|{:<40}|{:^20}|".format("Author name", "Articles count"))
        print('-' * 130)
        for columns in result:
            print("|{:<40}|{:^20}|".format(columns[0], columns[1]))
        print()

    def get_articles_by_week(self):
        result = self.__select_p.get_articles_by_week()
        print("Articles by week")
        print("|{:<40}|".format("Article name"))
        print('-' * 130)
        for columns in result:
            print("|{:<40}|".format(columns[0]))
        print()


