from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_package_form():
    response = client.get("/getPackageForm", params={"packageFormId": "form123"})
    assert response.status_code == OK
    assert response.json() == {"packageForm": {"packageFormId": "form123", "packageName": "Form Package", "name": "Sample Form", "typeformUrl": "http://example.com", "files": []}}