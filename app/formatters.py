from app.types import *


def package_to_fe_package(package: Package) -> FePackage:
    return FePackage(
        packageId=package.id,
        packageName=package.name,
        packageStatus=package.status.value,
        originalPdfPaths=package.original_pdf_paths,
        imagesWithBoxesPaths=package.images_with_boxes_paths,
        formFields=[FeFormField(**field.model_dump()) for field in package.form_fields],
        filledOutPackages=[FeFilledOutPackage(**filled_out.model_dump()) for filled_out in package.filled_out_packages],
        googleFormUrl=package.google_form_url
    )


def package_dict_to_fe_package_row(package_dict: dict) -> FePackageRow:
    return FePackageRow(
        packageId=package_dict['id'],
        packageName=package_dict['name'],
        packageStatus=package_dict['status']
    )
