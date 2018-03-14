import datetime


def get_articles_by_group(cur, group_name: str, from_time: str, to_time: str):
    """
    Получаем список популярных статей/репозиториев за неделю;
    """
    cur.execute("SELECT articles.title, articles.creation_date FROM articles "
                "RIGHT JOIN article_group a ON articles.id = a.article_id "
                "RIGHT JOIN groups g ON a.group_id = g.id "
                "WHERE group_name = '{}' AND creation_date BETWEEN '{}' AND '{}'"
                .format(group_name, from_time, to_time))

    return cur.fetchall()


def get_top_groups(cur):
    """
    Получаем топ 10 популярных хэш-тэгов, т.е. те, у которых больше всего статей/репозиториев;
    """

    cur.execute("SELECT group_name, COUNT(article_id) AS article_count FROM articles "
                "RIGHT JOIN article_group a ON articles.id = a.article_id "
                "RIGHT JOIN groups g ON a.group_id = g.id "
                "GROUP BY group_name "
                "ORDER BY article_count DESC LIMIT 10")

    return cur.fetchall()


def get_top_users(cur):
    """
     Получаем список самых активных пользователей, те, у которых больше всего статей
    """
    cur.execute("SELECT author_name, article_count FROM authors "
                "ORDER BY article_count DESC LIMIT 10")

    return cur.fetchall()


def get_articles_by_week(cur):
    """
    Получаем список популярных статей/репозиториев за неделю
    """
    current_date = datetime.datetime.today()
    week_ago = current_date.replace(day=current_date.day - 7)

    cur.execute("SELECT title FROM articles "
                "WHERE creation_date BETWEEN '{}' AND '{}'"
                .format(week_ago, current_date))

    return cur.fetchall()
