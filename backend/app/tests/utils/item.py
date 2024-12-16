import random
from sqlmodel import Session

from app import crud
from app.models import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    seller_id = user.id
    assert seller_id is not None
    name = random_lower_string()
    year = random.randrange(1980, 2024)
    selling_price = random.randrange(10000, 100000)
    km_driven = random.randrange(10000, 100000)
    fuel_type = random.choice(["Diesel", "Petrol"])
    transmission = random.choice(["Manual", "Automat"])
    owner_type = random.choice(["First Owner", "Second Owner", "Third owner"])
    mileage = random.randrange(10, 100)
    engine = random_lower_string()
    max_power = random.randrange(100, 1000)
    torque = random_lower_string()
    seats = random.randrange(2, 10)

    item_in = ItemCreate(
        name=name,
        year=year,
        selling_price=selling_price,
        km_driven=km_driven,
        fuel_type=fuel_type,
        transmission=transmission,
        owner_type=owner_type,
        mileage=mileage,
        engine=engine,
        max_power=max_power,
        torque=torque,
        seats=seats,
    )
    return crud.create_item(session=db, item_in=item_in, seller_id=seller_id)
