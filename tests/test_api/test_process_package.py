from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_package():
    response = client.post("/processPackage", json={"files": [], "name": "Test Package"})
    assert response.status_code == OK
    assert response.json() == {"packageRows": [{"packageId": "123", "packageName": "Test Package", "packageStatus": "complete"}]}