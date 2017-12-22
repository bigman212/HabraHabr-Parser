import re
import urllib.error
from urllib.request import urlopen


def _is_habrahabr(link: str) -> bool:
    return "habrahabr.ru/" in link


class HabrParser:
    def __init__(self, link: str):
        if _is_habrahabr(link):
            self.html_doc = self.__get_html(link)

            self.title = self.__parse_title()
            self.author = self.__parse_author()
            self.groups = self.__parse_groups()
            self.date = self.__parse_date()

        else:
            print("This link doesn't go to habrahabr!")
            input()
            exit(1)

    def __get_html(self, link):
        try:
            html_page = str(urlopen(link).read().decode('utf8'))
            return html_page
        except (urllib.error) as e:
            print(e)
            input()
            exit(1)

    def __parse_title(self) -> str:
        title_regex = '<span class="post__title-text">(.+?)</span>'
        title = re.findall(title_regex, self.html_doc)
        return title[0]

    def __parse_author(self) -> str:
        author_regex = '<span class="user-info__nickname user-info__nickname_small">(.+?)</span>'
        author = re.findall(author_regex, self.html_doc)
        return author[0]

    def __parse_groups(self) -> list:
        groups_regex = '<a .*? class="inline-list__item-link hub-link ".*?>(.+?)</a>'
        groups = re.findall(groups_regex, self.html_doc)
        return groups

    def __parse_date(self) -> str:
        date_regex = '<span class="post__time">(.+?)</span>'
        date = re.findall(date_regex, self.html_doc)
        date = date[0].strip().split(' ')
        day = date[0]
        month = date[1]
        year = date[2]
        if year == 'в':
            year = '2017'
        all_months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                      'августа', 'сентября', 'октября', 'ноября', 'декабря')

        if month in all_months:
            if all_months.index(month) > 8:
                month = "{}".format(all_months.index(month) + 1)

            else:
                month = "0{}".format(all_months.index(month) + 1)
        return "{}-{}-{}".format(year, month, day)

# TODO: добавить добавление статей
# def insertion():
#
#     # db.get_articles_by_group('Графический дизайн', '2016-01-01', '2018-01-01')
#     db.get_top_groups()
#     db.get_top_users()
#     db.get_articles_by_week()
#     current_link = "https://habrahabr.ru/company/dataline/blog/336828/"
#     habr_parser = HabrParser(current_link)
#
#     for group in habr_parser.groups:
#         db.insert_group(Group(group))
#
#     db.insert_author(Author(habr_parser.author))
#     db.insert_article(Article(current_link, habr_parser.title, habr_parser.author, habr_parser.date))
#
#     for group in habr_parser.groups:
#         db.insert_article_data(Article_Group(habr_parser.title, group))
#
#     db.commit()
