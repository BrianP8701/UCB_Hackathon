from http.client import OK
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_package_form_rows():
    response = client.get("/getPackageFormRows")
    assert response.status_code == OK
    assert response.json() == {"packageFormRows": [{"packageFormId": "form123", "packageName": "Form Package", "name": "Sample Form"}]}