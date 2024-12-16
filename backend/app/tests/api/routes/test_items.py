import uuid
from unittest.mock import patch
from datetime import datetime

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item


def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    mock_time = datetime(2023, 1, 1, 12, 0, 0)

    data = {
        "name": "Maruti Swift Dzire VDI",
        "year": 2014,
        "selling_price": 450000,
        "km_driven": 145500,
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "owner_type": "First Owner",
        "mileage": 23.4,
        "engine": "1248 CC",
        "max_power": 74,
        "torque": "190Nm@ 2000rpm",
        "seats": 5,
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["year"] == data["year"]
    assert "id" in content
    assert "seller_id" in content


def test_read_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item.name
    assert content["year"] == item.year
    assert content["id"] == str(item.id)
    assert content["seller_id"] == str(item.seller_id)


def test_read_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_read_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_item(db)
    create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"name": "Tesla X", "year": 2024}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["year"] == data["year"]
    assert content["id"] == str(item.id)
    assert content["seller_id"] == str(item.seller_id)


def test_update_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated name", "year": 0}
    response = client.put(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_delete_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item deleted successfully"


def test_delete_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_similar_items(client: TestClient, db: Session) -> None:
    item = create_random_item(db)
    for _ in range(10):
        create_random_item(db)
    response = client.get(f"{settings.API_V1_STR}/items/recommend/{item.id}/similar")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) > 0


def test_most_popular(client: TestClient, db: Session) -> None:
    for _ in range(10):
        create_random_item(db)
    response = client.get(f"{settings.API_V1_STR}/items/recommend/most_popular")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) > 0


def test_similar_query(client: TestClient, db: Session) -> None:
    for _ in range(10):
        create_random_item(db)
    data = {
        "min_year": 1994,
        "min_price": None,
        "max_price": None,
        "max_km_driven": None,
        "fuel_type": None,
    }
    response = client.post(
        url=f"{settings.API_V1_STR}/items/recommend/similar_query",
        params={"limit": 10, "offset": 0},
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) > 0
