import requests

url_get_package = "http://127.0.0.1:8000/getPackage"
url_get_packages_rows = "http://127.0.0.1:8000/getPackagesRows"
url_get_package_status = "http://127.0.0.1:8000/getPackageStatus"

package_id = "package9502cf28-98b5-4873-ab5e-4c98222f54c3"

response_get_package = requests.get(f"{url_get_package}?packageId={package_id}")
print(response_get_package.status_code)
print(response_get_package.json())

# response_get_packages_rows = requests.get(url_get_packages_rows)
# print(response_get_packages_rows.status_code)
# print(response_get_packages_rows.json())

# response_get_package_status = requests.get(f"{url_get_package_status}?packageId={package_id}")
# print(response_get_package_status.status_code)
# print(response_get_package_status.text)
