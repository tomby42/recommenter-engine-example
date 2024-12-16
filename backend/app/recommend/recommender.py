"""
This module should use ML to recommend similar items.
TODO - implement me, currently it is just mock
"""

import uuid
from typing import Sequence

from sqlalchemy.sql import func
from sqlmodel import Session, select
from app.models import Item, ItemQuery, Event


def find_most_popular_items(
    session: Session, limit: int = 10, offset: int = 0, user_id: uuid.UUID | None = None
) -> Sequence[Item]:
    """
    Returns top `limit` most popular items from offset `offset`.
    If `user_id` is defined personalize the selection.
    """
    if user_id is None:
        subquery = (
            select(Event.item_id, func.count(Event.id).label("popularity"))
            .group_by(Event.item_id)
            .subquery()
        )
    else:
        subquery = (
            select(Event.item_id, func.count(Event.id).label("popularity"))
            .where(Event.user_id == user_id)
            .group_by(Event.item_id)
            .subquery()
        )

    statement = (
        select(Item)
        .join(subquery, subquery.c.item_id == Item.id)
        .order_by(subquery.c.popularity.desc())
        .offset(offset)
        .limit(limit)
    )

    results = session.exec(statement).all()

    if len(results) < limit:
        statement = select(Item).limit(limit - len(results))
        results = [*results, *session.exec(statement).all()]

    return results


def find_similar_items(
    session: Session,
    item_id: uuid.UUID,
    limit: int = 10,
    offset: int = 0,
    user_id: uuid.UUID | None = None,
) -> Sequence[Item]:
    """
    Returns top `limit` most similar items to item `item_id` from offset `offset`.
    If `user_id` is defined personalize the selection.
    """
    item = session.get(Item, item_id)
    if item is None:
        return []

    query = ItemQuery(
        min_year=item.year,
        min_price=0,
        max_price=item.selling_price,
        max_km_driven=item.km_driven,
        fuel_type=item.fuel_type,
    )
    return find_similar_query(
        session, query, limit=limit, offset=offset, user_id=user_id
    )


def find_similar_query(
    session: Session,
    query: ItemQuery,
    limit: int = 10,
    offset: int = 0,
    user_id: uuid.UUID | None = None,
) -> Sequence[Item]:
    """
    Returns top `limit` most similar items to query `query` from offset `offset`.
    If `user_id` is defined personalize the selection.
    """
    stmt = select(Item)

    if query.min_year is not None:
        stmt = stmt.where(Item.year >= query.min_year)
    if query.min_price is not None:
        stmt = stmt.where(Item.selling_price >= query.min_price)
    if query.max_price is not None:
        stmt = stmt.where(Item.selling_price <= query.max_price)
    if query.max_km_driven is not None:
        stmt = stmt.where(Item.km_driven <= query.max_km_driven)
    if query.fuel_type is not None:
        stmt = stmt.where(Item.fuel_type == query.fuel_type)
    stmt = stmt.offset(offset).limit(limit)

    result = session.exec(stmt).all()
    return result
