from abc import ABC, abstractmethod
from typing import Any, Dict



class AbstractDatabase(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Initialization should remain flexible for subclass implementations.

    @abstractmethod
    def dispose_instance(self) -> None:
        """
        Disposes of the database instance, effectively clearing any existing connections.
        """
        pass

    @abstractmethod
    def insert(self, table_name: str, data: Dict) -> None:
        """
        Inserts a new data entry into the specified table.
        
        :param table_name: The table name.
        :param data: The dictionary to be serialized and stored, containing the 'id' key.
        """
        pass

    @abstractmethod
    def update(self, table_name: str, data: Dict) -> None:
        """
        Updates an existing data entry in the specified table.
        
        :param table_name: The table name.
        :param data: The updated dictionary to be serialized and stored, containing the 'id' key.
        """
        pass

    @abstractmethod
    def delete(self, table_name: str, data: Dict) -> None:
        """
        Deletes a data entry from the specified table using its identifier inside the data dict.
        
        :param table_name: The table name.
        :param data: The dictionary containing the 'id' key of the data to delete.
        """
        pass

    @abstractmethod
    def query(self, table_name: str, id: str) -> Dict:
        """
        Queries the database for a data entry by its identifier inside the data dict.
        
        :param table_name: The table name.
        :param id: The identifier of the data.
        :return: The deserialized dictionary representing the data.
        """
        pass

    @abstractmethod
    def exists(self, table_name: str, data: Dict) -> bool:
        """
        Checks if a data entry exists in the database using its identifier inside the data dict.
        
        :param table_name: The table name.
        :param data: The dictionary containing the 'id' key of the data.
        :return: True if the data exists, False otherwise.
        """
        pass

    @abstractmethod
    def execute_raw_query(self, query: str) -> Any:
        """
        Executes a raw SQL query against the database.
        
        :param query: The SQL query to execute.
        :return: The result of the query execution.
        """
        pass

    @abstractmethod
    def perform_transaction(self, operations: callable) -> None:
        """
        Performs a series of operations within a database transaction.
        
        :param operations: A callable that contains the operations to be performed.
        """
        pass

    @abstractmethod
    def clear_table(self, table_name: str, safety: str) -> None:
        """
        Clears all data from a specified table. This operation is irreversible.
        
        :param table_name: The table to be cleared.
        :param safety: A safety string that must match a specific value to confirm the operation.
        """
        pass