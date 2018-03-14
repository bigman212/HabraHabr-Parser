from habrparser.database_manager import DatabaseManager


def main():
    db = DatabaseManager("habr_db", 'postgres', 'QWERTY676')


if __name__ == '__main__':
    main()
