import os
import sqlite3
from sqlite3 import Connection


class DatabaseHandler:
    def __init__(self):
        self.db_file_path = "database"
        self.db_file = os.path.join(self.db_file_path, "database.db")
        self.connection: Connection | None = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, parameters=None):
        connection_already_existed = True
        if self.connection is None:
            # If no connection is available then create it
            self.connect()
            connection_already_existed = False

        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        self.connection.commit()

        if not connection_already_existed:
            # if the method has created the connection it can close, otherwise, it must leave that as it is
            self.disconnect()

    def fetch_data(self, query, parameters=None):
        self.connect()
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)

        # Allows accessing attributes by their name (e.g rows[0]['id'], rows[0]['pdf_link'], ...)
        self.cursor.row_factory = sqlite3.Row

        data = self.cursor.fetchall()
        self.disconnect()
        return data

    def table_exists(self, table_name):
        self.connect()
        q = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.execute_query(query=q, parameters=(table_name,))
        result = self.cursor.fetchone()
        self.disconnect()
        return result is not None

    def select_columns(self, table_name: str, columns: list, condition: str = "", condition_vals: tuple = None) -> list:
        """
        Selects the specified columns' values from the table based on the condition.
        Returns a list of rows, where each row is a tuple of column values.
        """
        # Generate the SQL query to select data
        column_names = ', '.join(columns)
        query = f"SELECT {column_names} FROM {table_name}"

        # Append the condition if provided
        if condition:
            query += f" WHERE {condition}"

        if condition and condition_vals is not None:
            return self.fetch_data(query=query, parameters=condition_vals)
        else:
            return self.fetch_data(query=query)

    def insert_data_into_table(self, table_name: str, data: dict) -> bool:
        """
        Inserts data into the specified table using the keys as column names and values as values.
        """
        self.connect()  # We establish we want to check the number of inserted rows before closing the connection

        # Generate the SQL query to insert data
        columns = ', '.join(data.keys())
        values = ', '.join('?' * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        params = tuple(data.values())

        try:
            self.execute_query(query=query, parameters=params)
        except sqlite3.Error as e:
            msg = f"Insertion failed: {e.__str__()}"
            print(msg)

            self.disconnect()  # disconnect before leaving the function

            # If error, return False
            return False

        # Get the rowcount
        if not self.cursor.rowcount > 0:
            msg = "Insertion failed."
            print(msg)

            self.disconnect()  # disconnect before leaving the function
            return False

        self.disconnect()  # disconnect before leaving the function

        return True

    def update_table(self, table_name: str, data: dict, condition: str = "", condition_vals: tuple = None) -> bool:
        """
        Updates the specified columns' values in the table based on the condition.
        """
        # Generate the SQL query to update data
        set_values = ', '.join([f"{column} = ?" for column in data])
        query = f"UPDATE {table_name} SET {set_values}"
        params = tuple(data.values())

        # Append the condition if provided
        if condition:
            query += f" WHERE {condition}"

            if condition_vals is not None:
                params = tuple(list(params) + list(condition_vals))

        try:
            self.execute_query(query=query, parameters=params)
        except sqlite3.Error as e:
            msg = f"Update failed: {e.__str__()}"
            print(f"query: {query}")
            print(f"params: {params}")
            print(msg)

            # If error, return False
            return False

        return True

    def delete_from_table(self, table_name: str, condition: str = "", condition_vals: tuple = None) -> bool:
        """
        Delete row(s) from a table based on the condition.
        """
        # Generate the SQL query to update data
        query = f"DELETE FROM {table_name}"

        # Append the condition if provided
        if condition:
            query += f" WHERE {condition}"

        try:
            if condition_vals is not None:
                self.execute_query(query=query, parameters=condition_vals)
            else:
                self.execute_query(query=query)
        except sqlite3.Error as e:
            msg = f"Delete failed: {e.__str__()}"
            print(msg)

            # If error, return False
            return False

        return True


def init_database() -> bool:
    """
    This function will initialize the database by creating a new database if it does not exist with all its tables.
    :return:
    """
    db_handler = DatabaseHandler()  # Initialize database instance

    # ------- Create tables if they don't exist
    # Creating table organizations_table
    table = "user"
    if not db_handler.table_exists(table_name=table):
        info = f"--------- Creating SQL Lite database table '{table}' in '{db_handler.db_file}'"
        print(info)

        try:
            # user_type = 'service-seeker', 'doctor'
            query = f'''CREATE TABLE {table} (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    firstname TEXT,
                                    lastname TEXT,
                                    title TEXT,
                                    institute TEXT,
                                    bio TEXT,
                                    username TEXT,
                                    password TEXT,
                                    user_type TEXT,
                                    joined_at TEXT
                                )'''

            db_handler.execute_query(query=query)
        except BaseException as e:
            msg = f"--------- An error occurred  while creating table '{table}' in SQL Lite database at " \
                  f"{db_handler.db_file} \n Error: {str(e)}"
            print(msg)

            # If error, close connection and return False
            # conn.close()
            return False

    # Creating table organizations_table
    # table = "doctor"
    # if not db_handler.table_exists(table_name=table):
    #     info = f"--------- Creating SQL Lite database table '{table}' in '{db_handler.db_file}'"
    #     print(info)
    #     try:
    #         query = f'''CREATE TABLE {table} (
    #                             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             firstname TEXT,
    #                             lastname TEXT,
    #                             title TEXT,
    #                             institute TEXT,
    #                             bio TEXT
    #                         )'''
    #
    #         db_handler.execute_query(query=query)
    #     except BaseException as e:
    #         msg = f"--------- An error occurred  while creating table '{table}' in SQL Lite database at " \
    #               f"{db_handler.db_file} \n Error: {str(e)}"
    #         print(msg)
    #
    #         # If error, close connection and return False
    #         # conn.close()
    #         return False

    # Creating table CONFIG["general"]["documents_table"]

    table = "chat"
    if not db_handler.table_exists(table_name=table):
        msg = f"--------- Creating SQL Lite database table '{table}' in '{db_handler.db_file}'"
        print(msg)

        try:
            query = f'''CREATE TABLE {table} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                doctor_id INTEGER,
                                is_bot_chat INTEGER
                            )'''

            # Commit the changes to the database
            # conn.commit()
            db_handler.execute_query(query=query)
        except BaseException as e:
            msg = f"--------- An error occurred  while creating table '{table}' in SQL Lite database at " \
                  f"{db_handler.db_file} \n Error: {str(e)}"
            print(msg)

            # If error, close connection and return False
            # conn.close()
            return False

    # Creating table temp_publications_urls_table
    table = "chat_message"
    if not db_handler.table_exists(table_name=table):
        msg = f"--------- Creating SQL Lite database table '{table}' in '{db_handler.db_file}'"
        print(msg)

        try:
            # sender_type: 'service-seeker', 'doctor', or 'bot'
            # receiver_type: 'service-seeker', 'doctor', or 'bot'
            # sender_id: if bot then -1
            # receiver_id: if bot then -1,
            query = f'''CREATE TABLE {table} (
                                    id INTEGER PRIMARY KEY,
                                    sender_type TEXT,
                                    receiver_type TEXT,
                                    sender_id INTEGER,
                                    receiver_id INTEGER,
                                    text TEXT,
                                    datetime TEXT
                                )'''

            # Commit the changes to the database
            # conn.commit()
            db_handler.execute_query(query=query)
        except BaseException as e:
            msg = f"--------- An error occurred  while creating table '{table}' in SQL Lite database at " \
                  f"{db_handler.db_file} \n Error: {str(e)}"
            print(msg)

            # If error, close connection and return False
            # conn.close()
            return False
    return True
