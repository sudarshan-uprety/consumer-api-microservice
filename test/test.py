from fastapi.testclient import TestClient

from main import server

client = TestClient(server)


def test_root():
    response = client.get("/je")
    print(response)
