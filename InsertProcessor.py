from entities import Author, Group, Article, Article_Group


# TODO : INSERT COMMITS AND EXCEPTIONS
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
        self.__cur.execute(f"SELECT article_count FROM {Author.TABLE_NAME} "
                           f"WHERE author_name = '{author.author_name}'")
        current_author_articles = self.__cur.fetchone()
        if current_author_articles:
            self.__add_article(current_author_articles[0], author)

        else:
            self.__create_new(author)

    def get_all(self):
        self.__cur.execute(f"SELECT * FROM {Author.TABLE_NAME}")
        for a in self.__cur.fetchall():
            print(a)

    def __create_new(self, author: Author):
        self.__cur.execute(f"INSERT INTO {Author.TABLE_NAME}(author_name, article_count) "
                           f"VALUES ('{author.author_name}', {author.article_count});")

    def __add_article(self, new_count: int, author: Author):
        author.article_count = new_count  # использовать ли абстракцию везде где можно
        self.__cur.execute(f"UPDATE {Author.TABLE_NAME} "
                           f"SET article_count = {author.article_count + 1} "
                           f"WHERE author_name = '{author.author_name}' ")


class _GroupsInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, group: Group):
        self.__cur.execute(f"SELECT article_count FROM {Group.TABLE_NAME} WHERE group_name = '{group.group_name}'")
        current_group_articles = self.__cur.fetchone()
        if current_group_articles:
            self.__add_article(current_group_articles[0], group)

        else:
            self.__create_new(group)

    def __add_article(self, new_count: int, group: Group):
        group.article_count = new_count
        self.__cur.execute(f"UPDATE {GROUP.TABLE_NAME} "
                           f"SET article_count = {GROUP.article_count + 1} "
                           f"WHERE group_name = '{group.group_name}' ")

    def __create_new(self, group: Group):
        self.__cur.execute(f"INSERT INTO {GROUP.TABLE_NAME}(group_name, article_count) "
                           f"VALUES ('{group.group_name}', {GROUP.article_count});")

    def get_all(self):
        self.__cur.execute(f"SELECT * FROM {Group.TABLE_NAME}")
        for a in self.__cur.fetchall():
            print(a)


class _ArticleInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, article: Article):
        self.__cur.execute(f"SELECT id FROM {Article.TABLE_NAME} WHERE title = '{article.title}'")
        current_article_id = self.__cur.fetchone()
        if current_article_id:
            print("ALREADY IN DATABASE")
        else:
            self.__create_new(article)

    def __create_new(self, article: Article):
        self.__cur.execute(f"SELECT id FROM {Author.TABLE_NAME} WHERE author_name = '{article.author_name}'")
        current_author_id = self.__cur.fetchone()[0]
        self.__cur.execute(f"INSERT INTO {Article.TABLE_NAME}(link, title, author_id, creation_date) "
                           f"VALUES ('{article.link}', '{article.title}', {current_author_id}, '{article.creation_date}');")

    def get_all(self):
        self.__cur.execute(f"SELECT * FROM {Article.TABLE_NAME}")
        for a in self.__cur.fetchall():
            print(a)


class _ArticleGroupInsert:
    def __init__(self, cur):
        self.__cur = cur

    def insert(self, article_group: Article_Group):
        article_id = self.find_article_id(article_group.article_name)
        group_id = self.find_group_id(article_group.group_name)
        self.__cur.execute(f"INSERT INTO {Article_Group.TABLE_NAME}(article_id, group_id) "
                           f"VALUES ({article_id}, {group_id})")

    def find_article_id(self, article_name):
        self.__cur.execute(f"SELECT id FROM {Article.TABLE_NAME} WHERE title = '{article_name}'")
        current_id = self.__cur.fetchone()[0]
        return current_id

    def find_group_id(self, group_name):
        self.__cur.execute(f"SELECT id FROM {Group.TABLE_NAME} WHERE group_name = '{group_name}'")
        current_id = self.__cur.fetchone()[0]
        return current_id
