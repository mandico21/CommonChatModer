import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
            self,
            sql: str,
            parameters: tuple = None,
            fetchone=False,
            fetchall=False,
            commit=False,
    ):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_stickers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS BannedStickers(
            set_name varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    def create_table_chat_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ChatAdmins(
            chat_id INTEGER NOT NULL,
            admin_id INTEGER NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def block_sticker(self, set_name: str):

        sql = """
        INSERT INTO BannedStickers(set_name) VALUES(?)
        """
        self.execute(sql, parameters=(set_name,), commit=True)

    def select_all_sets(self):
        sql = """
        SELECT * FROM BannedStickers
        """
        return self.execute(sql, fetchall=True)

    def select_all_chat_admins(self, chat_id: int):
        sql = """
        SELECT admin_id FROM ChatAdmins
        WHERE chat_id = ?
        """
        return self.execute(sql, (chat_id,), fetchall=True)

    def add_chat_admin(self, chat_id: int, admin_id: int):
        sql = """
        INSERT INTO ChatAdmins(chat_id, admin_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(chat_id, admin_id), commit=True)

    def del_chat_admin(self, chat_id: int, admin_id: int):
        sql, parameters = self.format_args(
            sql="DELETE FROM ChatAdmins WHERE ",
            parameters={'chat_id': chat_id, 'admin_id': admin_id}
        )
        self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )
