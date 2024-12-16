from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import UserCreate
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import random_email, random_lower_string


def test_create_event(client: TestClient, db: Session) -> None:
    user = crud.create_user(
        session=db,
        user_create=UserCreate(email=random_email(), password=random_lower_string()),
    )
    item = create_random_item(db)

    data = {
        "user_id": str(user.id),
        "item_id": str(item.id),
        "event_type": "click",
        "event_value": None,
    }
    response = client.post(
        f"{settings.API_V1_STR}/events/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["user_id"] == data["user_id"]
    assert content["item_id"] == data["item_id"]
    assert content["event_type"] == data["event_type"]
    assert "id" in content
    assert "timestamp" in content
