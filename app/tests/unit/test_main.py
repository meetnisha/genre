from fastapi import FastAPI
from fastapi.testclient import TestClient
from pathlib import Path
import os 
import pytest
from httpx import AsyncClient

from ...main import app

app = FastAPI()
client = TestClient(app)
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

base_url = 'http://localhost:8000/'

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_form_post():
    _test_upload_file = Path(CURRENT_FOLDER + '/data/', 'test.csv')
    _files = {'upload_file': _test_upload_file.open('rb')}
    with TestClient(app) as client:
        response = client.post(base_url + '/upload',
                                files=_files)
        print(response.json())
        assert response.status_code == 200

    # remove the test file from the config directory
    #_copied_file = Path(CURRENT_FOLDER + '/data/', 'test.csv')
    #_copied_file.unlink()

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/search/?filter=0")
    print(response.json())
    assert response.status_code == 200
    

""" def test_search_genre():
    response = client.get("/search/?filter=0", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

    response = client.get("/search/?filter=0",
        headers={"X-Token": "coneofsilence"},
        filter = "classic pop and rock"
    )
    print(response.json())
    assert response.status_code == 200 """
    