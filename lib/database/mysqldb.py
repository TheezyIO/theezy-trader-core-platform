from lib.common.logger import Logger
from mysql.connector import connect

import os

logger = Logger('database.mysqldb')


def missing_env_var(var):
    logger.error(f'Missing environment variable: {var}')

def quote(s):
    return f"'{s}'"

class MySQLClient:

    def __init__(self, host=None, user=None, password=None, database=None):
        self.host = host or os.getenv('MYSQL_HOST')
        self.user = user or os.getenv('MYSQL_USER')
        self.password = password or os.getenv('MYSQL_PASSWORD')
        self.database = database or os.getenv('MYSQL_DATABASE')
        self.connection = None
        self.cursor = None

    def is_connected(self):
        return self.connection is not None

    def connect(self):
        if not self.host:
            missing_env_var('MYSQL_HOST')
        if not self.user:
            missing_env_var('MYSQL_USER')
        if not self.database:
            missing_env_var('MYSQL_DATABASE')
        if not self.password:
            missing_env_var('MYSQL_PASSWORD')
        if not self.connection:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

    def get_results(self):
        if not self.cursor:
            return None

        column_names = self.cursor.column_names
        results = self.cursor.fetchall()

        self.cursor.close()
        self.cursor = None

        json_results = []
        for result in results:
            result_json = {}
            for i in range(len(column_names)):
                result_json[column_names[i]] = result[i]
            json_results.append(result_json)

        return json_results

    def query(self, query):
        if not self.is_connected():
            self.connect()

        self.cursor = self.connection.cursor()
        logger.debug(f'Executing query: {query}')
        self.cursor.execute(query)

        return self.get_results()

    def insert(self, table_name, rows):
        inserted_ids = []
        if not rows:
            return inserted_ids

        if not self.is_connected():
            self.connect()

        self.cursor = self.connection.cursor()
        for row in rows:
            columns = row.keys()
            values = ', '.join(map(lambda c: quote(row[c]), columns))
            column_fields  = ', '.join(columns)
            logger.debug(f'Executing INSERT INTO {table_name} ({column_fields}) VALUES ({values})')
            self.cursor.execute(f'INSERT INTO {table_name} ({column_fields}) VALUES ({values})')
            inserted_ids.append(self.cursor.lastrowid)

        self.connection.commit()

        self.cursor.close()
        self.cursor = None

        return inserted_ids

    def update(self, table_name, update, where_clause):
        if not update:
            return

        if not self.is_connected():
            self.connect()

        self.cursor = self.connection.cursor()

        columns = update.keys()
        values = ', '.join(map(lambda c: f'{c} = {quote(update[c])}', columns))
        logger.debug(f'Executing UPDATE {table_name} SET {values} WHERE {where_clause}')
        self.cursor.execute(f'UPDATE {table_name} SET {values} WHERE {where_clause}')

        self.connection.commit()

        self.cursor.close()
        self.cursor = None

    def __del__(self):
        if self.connection:
            self.connection.close()
