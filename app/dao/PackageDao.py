from app.database import *
import json
import logging
from app.types import *
from app.formatters import package_dict_to_fe_package_row

database = Database()
storage = Storage()

class PackageDao:
    @classmethod
    def upsert(cls, package: Package) -> None:
        package_as_dict = package.model_dump()
        package_as_dict['status'] = package_as_dict['status'].value
        form_fields = []
        for form_field in package_as_dict["form_fields"]:
            form_field['form_field_type'] = form_field['form_field_type'].value
            form_fields.append(form_field)
        package_as_dict["form_fields"] = form_fields
        database.upsert("packages", package_as_dict)

    @classmethod
    def get_package(cls, package_id: str) -> Package:
        package = database.read("packages", package_id)
        if package:
            package['packageId'] = package_id
            return Package(**package)
        else:
            raise KeyError(f"No package found with ID: {package_id}")

    @classmethod
    def get_package_rows(cls) -> List[FePackageRow]:
        package_rows = database.get_all("packages")
        logging.info(f'package_rows: {package_rows}')
        return [package_dict_to_fe_package_row(package_dict) for package_dict in package_rows]
