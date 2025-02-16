import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

def test_create_item_success():
    payload = {
        "sellerID": 123456,
        "name": "Test Item",
        "price": 100,
        "statistics": {
            "contacts": 3,
            "likes": 10,
            "viewCount": 50
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=payload)

    assert response.status_code == 200, "Ожидался статус 200"
    response_data = response.json()
    assert "status" in response_data, "Ответ не содержит поле 'status'"

    assert "Сохранили объявление" in response_data["status"], "Статус ответа не содержит 'Сохранили объявление'"

    # Извлекаем ID из строки
    item_id = response_data["status"].split(" - ")[-1]
    assert len(item_id) > 0, "Не удалось извлечь ID объявления"


def test_create_item_without_statistics():
    payload = {
        "sellerID": 123456,
        "name": "Test Item",
        "price": 100
    }

    response = requests.post(f"{BASE_URL}/item", json=payload)

    assert response.status_code == 200, "Ожидался статус 200 OK"

    response_data = response.json()
    assert "status" in response_data, "Ответ не содержит поле 'status'"

    assert "Сохранили объявление" in response_data["status"], "Статус ответа не содержит 'Сохранили объявление'"

    # Извлекаем ID объявления
    item_id = response_data["status"].split(" - ")[-1]
    assert len(item_id) > 0, "Не удалось извлечь ID объявления"


def test_create_item_without_name():
    payload = {
        "sellerID": 123456,
        "price": 100,
        "statistics": {
            "contacts": 3,
            "likes": 10,
            "viewCount": 50
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=payload)

    assert response.status_code == 400, "Ожидался статус 400"
    assert "error" in response.json(), "В ответе должен быть текст ошибки"


def test_create_item_negative_price():
    payload = {
        "sellerID": 123456,
        "name": "Test Item",
        "price": -100,
        "statistics": {
            "contacts": 3,
            "likes": 10,
            "viewCount": 50
        }
    }

    response = requests.post(f"{BASE_URL}/item", json=payload)

    assert response.status_code == 400, "Ожидался статус 400"
    assert "error" in response.json(), "В ответе должен быть текст ошибки"
