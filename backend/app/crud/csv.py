import uuid

from sqlmodel import Session
import pandas as pd
from app.models import Item


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare dataframe created from CSV file to import to db.
    """
    df["fuel_type"] = df["fuel"]
    df["owner_type"] = df["owner"]
    df.drop(columns=["seller_type", "fuel", "owner"], inplace=True)
    df = df.drop_duplicates()
    df.loc[:, "mileage"] = (
        df["mileage"]
        .str.replace(r"[^0-9.]+", "", regex=True)
        .replace(r"^$", "0", regex=True)
        .astype(float)
    )
    df.loc[:, "max_power"] = (
        df["max_power"]
        .str.replace(r"[^0-9.]+", "", regex=True)
        .replace(r"^$", "0", regex=True)
        .astype(float)
    )
    df.loc[df["seats"].isna(), "seats"] = 4

    return df


def import_csv(csv_path: str, session: Session, current_user_id: uuid.UUID):
    """
    Import CSV file into db.
    """
    df = pd.read_csv(csv_path)
    df = preprocess_df(df)
    records = [
        Item(seller_id=current_user_id, **row.to_dict()) for _, row in df.iterrows()
    ]
    session.add_all(records)
    session.commit()
