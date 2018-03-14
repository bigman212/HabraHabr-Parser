class Article:
    TABLE_NAME = 'articles'

    def __init__(self, link: str, title: str, author_name: str, date: str):
        self.link = link
        self.title = title
        self.author_id = 0
        self.author_name = author_name
        self.creation_date = date


class Author:
    TABLE_NAME = 'authors'

    def __init__(self, author: str):
        self.author_name = author
        self.article_count = 1


class Group:
    TABLE_NAME = 'groups'

    def __init__(self, group_name):
        self.group_name = group_name
        self.article_count = 1


class Article_Group:
    TABLE_NAME = 'article_group'

    def __init__(self, article_name, group_name):
        self.article_name = article_name
        self.group_name = group_name
