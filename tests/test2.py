import requests

url_get_package = "http://127.0.0.1:8000/getPackage"
url_get_packages_rows = "http://127.0.0.1:8000/getPackagesRows"
url_get_package_status = "http://127.0.0.1:8000/getPackageStatus"

package_id = "packagea5f2a5fd-21fe-47ac-a61a-4f2274c9ebbd"

response_get_package = requests.get(f"{url_get_package}?packageId={package_id}")
print(response_get_package.status_code)
print(response_get_package.json())

response_get_packages_rows = requests.get(url_get_packages_rows)
print(response_get_packages_rows.status_code)
print(response_get_packages_rows.json())

response_get_package_status = requests.get(f"{url_get_package_status}?packageId={package_id}")
print(response_get_package_status.status_code)
print(response_get_package_status.text)
