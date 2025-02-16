import requests

BASE_URL = "https://qa-internship.avito.com/api/1"


def test_get_existing_item_statistics():
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

    response = requests.get(f"{BASE_URL}/statistic/{created_item_id}")

    assert response.status_code == 200, "Ожидался статус 200 при получении статистики"

    response_data = response.json()
    assert isinstance(response_data, list), "Ожидался список статистики"

    stats_data = response_data[0]

    assert stats_data["likes"] == create_payload["statistics"]["likes"], "Количество лайков не совпадает"
    assert stats_data["viewCount"] == create_payload["statistics"]["viewCount"], "Количество просмотров не совпадает"
    assert stats_data["contacts"] == create_payload["statistics"]["contacts"], "Количество контактов не совпадает"

def test_get_non_existing_item_statistics():
    non_existing_id = "00000000-0000-0000-0000-000000000000"

    response = requests.get(f"{BASE_URL}/statistic/{non_existing_id}")

    assert response.status_code == 404, "Ожидался статус 404 для несуществующего объявления"

def test_get_statistics_invalid_id():
    invalid_id = "123"

    response = requests.get(f"{BASE_URL}/statistic/{invalid_id}")

    assert response.status_code == 400, "Ожидался статус 400 для некорректного ID"
