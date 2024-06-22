from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_package_form():
    response = client.post("/createPackageForm", json={"name": "New Form", "packageId": "form123"})
    assert response.status_code == OK
    assert response.json() == {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": "New Form"}]}
