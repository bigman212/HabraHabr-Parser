from urllib.request import urlopen
import re
import urllib3.exceptions, urllib.error
from DatabaseManager import *


# сделать сущности
# попробывать re

def is_habrahabr(link: str) -> bool:
    return "habrahabr.ru/" in link


class HabrParser:
    def __init__(self, link: str):
        if is_habrahabr(link):
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


# ip.insert_author(Author(current_author))
# ip.insert_article(Article(current_link, current_title, current_author, '10-11-2017'))


if __name__ == '__main__':
    db = DatabaseManager()
    current_link = ""
    habr_parser = HabrParser(current_link)
    for group in habr_parser.groups:
        db.insert_article_data(Article_Group(habr_parser.title, group))
    db.commit()
