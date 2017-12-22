from entities import Author, Group, Article, Article_Group


# TODO : INSERT ABSTRACT CALSS AND EXCEPTIONS
class InsertProcessor:  # или INSERTProcessor
    def __init__(self, db_conn):
        self.conn = db_conn
        cur = self.conn.cursor()

        self.__authors_insert = _AuthorsInsert(cur)
        self.__groups_insert = _GroupsInsert(cur)
        self.__articles_insert = _ArticleInsert(cur)
        self.__article_group_insert = _ArticleGroupInsert(cur)

    def insert_author(self, author: Author):
        self.__authors_insert.insert(author)

    def insert_group(self, group: Group):
        self.__groups_insert.insert(group)

    def insert_article(self, article: Article):
        self.__articles_insert.insert(article)

    def insert_article_group(self, article_group: Article_Group):
        self.__article_group_insert.insert(article_group)


class _AuthorsInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, author: Author):
        self.__cur.execute("SELECT article_count FROM {} "
                           "WHERE author_name = '{}'".format(Author.TABLE_NAME, author.author_name))
        current_author_articles = self.__cur.fetchone()
        if current_author_articles:
            self.__add_article(current_author_articles[0], author)
        else:
            self.__create_new(author)

    def __create_new(self, author: Author):
        self.__cur.execute("INSERT INTO {}(author_name, article_count) "
                           "VALUES ('{}', {})"
                           .format(Author.TABLE_NAME, author.author_name, author.article_count))

    def __add_article(self, new_count: int, author: Author):
        author.article_count = new_count  # использовать ли абстракцию везде где можно
        self.__cur.execute("UPDATE {} "
                           "SET article_count = {} "
                           "WHERE author_name = '{}' "
                           .format(Author.TABLE_NAME, author.article_count + 1, author.author_name))


class _GroupsInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, group: Group):
        self.__cur.execute("SELECT article_count FROM {} WHERE group_name = '{}'"
                           .format(Group.TABLE_NAME, group.group_name))
        current_group_articles = self.__cur.fetchone()
        if current_group_articles:
            self.__add_article(current_group_articles[0], group)

        else:
            self.__create_new(group)

    def __add_article(self, new_count: int, group: Group):
        group.article_count = new_count
        self.__cur.execute("UPDATE {} "
                           "SET article_count = {} "
                           "WHERE group_name = '{}'"
                           .format(Group.TABLE_NAME, group.article_count + 1, group.group_name))

    def __create_new(self, group: Group):
        self.__cur.execute("INSERT INTO {}(group_name, article_count) "
                           "VALUES ('{}', {})"
                           .format(Group.TABLE_NAME, group.group_name, group.article_count))



class _ArticleInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, article: Article):
        query = "SELECT id FROM {} WHERE title = '{}'".format(Article.TABLE_NAME, article.title)
        self.__cur.execute(query)
        current_article_id = self.__cur.fetchone()
        if current_article_id:
            print("ALREADY IN DATABASE")
        else:
            self.__create_new(article)

    def __create_new(self, article: Article):
        self.__cur.execute("SELECT id FROM {} WHERE author_name = '{}'"
                           .format(Author.TABLE_NAME, article.author_name))
        current_author_id = self.__cur.fetchone()[0]
        self.__cur.execute("INSERT INTO {}(link, title, author_id, creation_date) "
                           "VALUES ('{}', '{}', {}, '{}')"
                           .format(Article.TABLE_NAME, article.link, article.title, current_author_id,
                                   article.creation_date))

class _ArticleGroupInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, article_group: Article_Group):
        article_id = self.find_article_id(article_group.article_name)
        group_id = self.find_group_id(article_group.group_name)
        self.__cur.execute("INSERT INTO {}(article_id, group_id) "
                           "VALUES ({}, {})"
                           .format(Article_Group.TABLE_NAME, article_id, group_id))

    def find_article_id(self, article_name):
        self.__cur.execute("SELECT id FROM {} WHERE title = '{}'"
                           .format(Article.TABLE_NAME, article_name))
        current_id = self.__cur.fetchone()[0]
        return current_id

    def find_group_id(self, group_name):
        self.__cur.execute("SELECT id FROM {} WHERE group_name = '{}'"
                           .format(Group.TABLE_NAME, group_name))
        current_id = self.__cur.fetchone()[0]
        return current_id
