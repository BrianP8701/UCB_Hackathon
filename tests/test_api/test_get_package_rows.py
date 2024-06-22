from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_packages_rows():
    response = client.get("/getPackagesRows")
    assert response.status_code == OK
    assert response.json() == {"packageRows": [{"packageId": "123", "packageName": "Sample Package", "packageStatus": "complete"}]}