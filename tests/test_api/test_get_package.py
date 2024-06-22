from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_package():
    response = client.get("/getPackage", params={"packageId": "123"})
    assert response.status_code == OK
    assert response.json() == {"package": {"packageId": "123", "packageName": "Sample Package", "packageStatus": "complete", "rawFiles": [], "labeledFiles": []}}