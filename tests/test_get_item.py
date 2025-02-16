import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

def test_get_existing_item():
    create_payload = {
        "sellerID": 123456,
        "name": "Test Item",
        "price": 100,
        "statistics": {
            "contacts": 3,
            "likes": 10,
            "viewCount": 50
        }
    }

    create_response = requests.post(f"{BASE_URL}/item", json=create_payload)
    assert create_response.status_code == 200, "Ожидался статус 200 при создании"

    created_item_id = create_response.json()["status"].split(" - ")[-1]

    response = requests.get(f"{BASE_URL}/item/{created_item_id}")

    assert response.status_code == 200, "Ожидался статус 200 при получении объявления"

    response_data = response.json()
    assert isinstance(response_data, list), "Ожидался список объявлений в ответе API"

    item_data = response_data[0]
    assert item_data["id"] == created_item_id, "ID объявления не совпадает"
    assert item_data["name"] == create_payload["name"], "Название объявления не совпадает"
    assert item_data["price"] == create_payload["price"], "Цена объявления не совпадает"


def test_get_non_existing_item():
    non_existing_id = "00000000-0000-0000-0000-000000000000"

    response = requests.get(f"{BASE_URL}/item/{non_existing_id}")

    assert response.status_code == 404, "Ожидался статус 404 для несуществующего объявления"


def test_get_item_invalid_id():
    invalid_id = "123"

    response = requests.get(f"{BASE_URL}/item/{invalid_id}")

    assert response.status_code == 400, "Ожидался статус 400 для некорректного ID"
