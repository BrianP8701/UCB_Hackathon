from app.types import *
from app.utils import get_path_from_file_id


def package_to_fe_package(package: Package) -> FePackage:
    filledOutPackages = []
    for filled_out_package in package.filled_out_packages:
        filledOutPackages.append(FeFilledOutPackage(
            email=filled_out_package.email,
            pdfPath=get_path_from_file_id(filled_out_package.filled_out_pdf_id)
        ))
    return FePackage(
        packageId=package.id,
        packageName=package.name,
        packageStatus=package.status.value,
        originalPdfPath=get_path_from_file_id(package.original_pdf_id),
        imagesWithBoxesPaths=[get_path_from_file_id(image_id) for image_id in package.images_with_boxes_ids],
        filledOutPackages=filledOutPackages,
        typeformUrl=package.typeform_url,
        typeformId=package.typeform_id
    )


def package_dict_to_fe_package_row(package_dict: dict) -> FePackageRow:
    return FePackageRow(
        packageId=package_dict['id'],
        packageName=package_dict['data']['name'],
        packageStatus=package_dict['data']['status']
    )
