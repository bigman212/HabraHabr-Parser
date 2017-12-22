import psycopg2

from habrparser.database_manager import DatabaseManager


def get_connection(db_name, user, password):
    try:
        conn = psycopg2.connect(dbname=db_name, user=user, password=password)
        return conn
    except psycopg2.Error as e:
        print(e)
        print("Check pass/login/conn")
        input()
        exit(1)


def main():
    db = DatabaseManager(get_connection("habr_db", 'postgres', 'QWERTY676'))
    db.get_articles_by_group('Программирование', '2016-01-01', '2018-01-01')


if __name__ == '__main__':
    main()
