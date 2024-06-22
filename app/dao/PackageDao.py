from app.types import Package
from app.database.Database import Database
import json

class PackageDao:
    def __init__(self, database: Database):
        self.database = database
        self.table_name = 'packages'

    def upsert_package(self, package: Package) -> None:
        package_dict = package.dict()
        package_id = package_dict.pop('packageId')
        serialized_data = json.dumps(package_dict)
        if self.database.exists(self.table_name, package_id):
            self.database.update(self.table_name, {'id': package_id, 'data': serialized_data})
        else:
            self.database.insert(self.table_name, {'id': package_id, 'data': serialized_data})

    def get_package(self, package_id: str) -> Package:
        result = self.database.query(self.table_name, package_id)
        if result:
            package_data = json.loads(result['data'])
            package_data['packageId'] = package_id
            return Package(**package_data)
        else:
            raise KeyError(f"No package found with ID: {package_id}")
