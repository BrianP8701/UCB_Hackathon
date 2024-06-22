from typing import Any, Dict, Callable
import sqlite3
import json
import os
from dotenv import load_dotenv

from app.database.abstract import AbstractDatabase

load_dotenv()
db_connection_string: str | None = os.getenv("DB_CONNECTION_STRING")

class Database(AbstractDatabase):
    _instance = None
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            if db_connection_string is None:
                raise ValueError("DB_CONNECTION_STRING environment variable is not set")
            cls._instance.connection = sqlite3.connect(db_connection_string, check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self, tables: list = []):
        for table in tables:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table} (id TEXT PRIMARY KEY, data TEXT)"
            )
        self.connection.commit()

    def dispose_instance(self) -> None:
        self.connection.close()

    def create(self, table_name: str, data: Dict) -> None:
        data_id = data.pop('id')
        serialized_data = json.dumps(data)
        self.cursor.execute(
            f"INSERT INTO {table_name} (id, data) VALUES (?, ?)",
            (data_id, serialized_data)
        )
        self.connection.commit()

    def update(self, table_name: str, data: Dict) -> None:
        data_id = data['id']
        serialized_data = json.dumps(data)
        self.cursor.execute(
            f"UPDATE {table_name} SET data = ? WHERE id = ?",
            (serialized_data, data_id)
        )
        self.connection.commit()

    def delete(self, table_name: str, data: Dict) -> None:
        data_id = data.pop('id')
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE id = ?",
            (data_id,)
        )
        self.connection.commit()

    def read(self, table_name: str, id: str) -> Dict:
        self.cursor.execute(
            f"SELECT data FROM {table_name} WHERE id = ?",
            (id,)
        )
        result = self.cursor.fetchone()
        if result:
            result = json.loads(result[0])
            result['id'] = id
            return result
        else:
            raise KeyError(f"No data found for ID: {id} in table: {table_name}")

    def exists(self, table_name: str, id: str) -> bool:
        self.cursor.execute(
            f"SELECT 1 FROM {table_name} WHERE id = ?",
            (id,)
        )
        return bool(self.cursor.fetchone())

    def execute_raw_query(self, query: str) -> Any:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def perform_transaction(self, operations: Callable[[], None]) -> None:
        try:
            self.connection.execute("BEGIN")
            operations()
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def clear_table(self, table_name: str, safety: str) -> None:
        if safety == "CONFIRM":
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.connection.commit()
        else:
            raise ValueError("Safety check failed; clear_table operation aborted.")

    def get_all(self, table_name: str) -> list:
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        return [{'id': row[0], 'data': json.loads(row[1])} for row in rows]