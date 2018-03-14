import re
import urllib.error
from urllib.request import urlopen


def _is_habrahabr(link: str) -> bool:
    return "habrahabr.ru/" in link


class HabrParser:
    """
    The HabrParser object is used to get all the necessary information from the Habrahabr article
    such as : article title, article author, article groups (hashtags), creation date.
    Needed information is kept in variables below. All these variables are getting their values
    as a return result from private methods.

    ::file:: re.py is used for parsing

    Constructor has only one parameter - link to the Habrahabr article. This link is being checked, and
    if it doesn't go to the Habrahabr site - it writes mistake and exits.
    For usage - you just need to create :class:'HabrParser' instance and pass the link like this::

           from HabrParser import HabrParser
           parser = HabrParser('your_link_here')

    After that, you can get information about the article like this::

           article_title = parser.title
           creation_date = parser.date
           ...

       """
    def __init__(self, link: str):
        if _is_habrahabr(link):
            self.html_doc = self.__get_html(link)

            self.link = link
            self.title = self.__parse_title()
            self.author = self.__parse_author()
            self.groups = self.__parse_groups()
            self.date = self.__parse_date()

        else:
            print("This link doesn't go to habrahabr!")
            input()
            exit(1)

    def __get_html(self, link):
        """
        Gets a raw string html copy of web-page.
        Uses :file:'urllib.request' to get web-page content.
        :param link: link to the web-page
        :return: str representation of html page
         """
        try:
            html_page = str(urlopen(link).read().decode('utf-8'))
            return html_page
        except urllib.error.HTTPError as e:
            print("Something with HTTP: ", e)
            input()
            exit(1)
        except urllib.error.URLError as e:
            print("Something with URL: ", e)
            input()
            exit(1)

    def __parse_title(self) -> str:
        """
        Parses the title of habrahabr article with the :file:'re.py' and :meth: findall.
        Gets the first result of the :meth:'findall' query. Example::

            example_title = "<span class="post__title_text">Retrofit 2 with Android</span>"
            title = re.findall(:var:'title_regex') # returns ('Retrofit 2 with Android')

        :return: title of the article
        """
        title_regex = '<span class="post__title-text">(.+?)</span>'
        title = re.findall(title_regex, self.html_doc)
        return title[0]

    def __parse_author(self) -> str:
        """
        Works same as :meth:'__parse_title', but searches with the different regexp for an author.
        :return: author of the article
        """
        author_regex = '<span class="user-info__nickname user-info__nickname_small">(.+?)</span>'
        author = re.findall(author_regex, self.html_doc)
        return author[0]

    def __parse_groups(self) -> list:
        """
        Parses the groups/hashtags that characterize article. Example::
            tag_1 = '<a *attributes* class="inline-list__item-link hub-link " *attributes*>Java</a>'
            tag_2 = '<a *attributes* class="inline-list__item-link hub-link " *attributes*>Kotlin</a>'
            groups = re.findall(:var:'groups_regex') # returns ('Java', 'Kotlin')
        :return: list of all groups
        """
        groups_regex = '<a .*? class="inline-list__item-link hub-link ".*?>(.+?)</a>'
        groups = re.findall(groups_regex, self.html_doc)
        return groups

    def __parse_date(self) -> str:
        """
        Searches article creation date and converts it to the format 'YYYY-MM-DD'
        At first gets date in format like 'day month_name year(optional)' After spliting the string into a list
        and checking each element - returns formatted string.
        If the second element of the list is a char 'в' it means that article creation year = current year = 2017
        :return: formatted str date in 'YYY-MM-DD'
        """
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

    # def get_values_dict(self) -> dict:
    #     values_dict = {}
    #     values_dict["link"] = self.link
    #     values_dict["author"] = self.author
    #     values_dict["groups"] = self.groups
    #     values_dict["creation_date"] = self.date
    #     return values_dict
