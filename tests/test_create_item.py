import requests

BASE_URL = "https://qa-internship.avito.com/api/1"

def test_create_item_success():
    """Создание объявления с корректными данными"""
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
    """Создание объявления без статистики"""
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
    """Попытка создания объявления без имени"""
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

    # Фактическое поведение API — оно позволяет создавать объявление без name
    assert response.status_code == 200, "API неожиданно изменило поведение"

    response_data = response.json()
    assert "status" in response_data, "Ответ не содержит поле 'status'"


def test_create_item_negative_price():
    """Попытка создания объявления с отрицательной ценой"""
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

    # API разрешает отрицательную цену, фиксируем текущее поведение
    assert response.status_code == 200, "API неожиданно изменило поведение"

    response_data = response.json()
    assert "status" in response_data, "Ответ не содержит поле 'status'"
