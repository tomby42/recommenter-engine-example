from typing import Any
import uuid

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import ItemsPublic, ItemQuery
from app.recommend import (
    find_similar_items,
    find_most_popular_items,
    find_similar_query,
)

router = APIRouter(prefix="/items/recommend", tags=["items/recommend"])


@router.get("/{item_id}/similar", response_model=ItemsPublic)
def similar_items(
    session: SessionDep, item_id: uuid.UUID, limit: int = 10, offset: int = 0
) -> Any:
    """
    Retrieve top `limit` similar items to `item_id`
    """
    items = find_similar_items(session, item_id=item_id, limit=limit, offset=offset)
    return ItemsPublic(data=items, count=len(items))


@router.get("/most_popular", response_model=ItemsPublic)
def most_popular_items(session: SessionDep, limit: int = 10, offset: int = 0) -> Any:
    """
    Retrieve `limit` most popular items.
    """
    items = find_most_popular_items(session, limit=limit, offset=offset)
    return ItemsPublic(data=items, count=len(items))


@router.post("/similar_query", response_model=ItemsPublic)
def similar_query(
    session: SessionDep, query: ItemQuery, limit: int = 10, offset: int = 0
) -> Any:
    """
    Retrieve `count` most similar items to query `query` .
    """

    items = find_similar_query(session, query=query, limit=limit, offset=offset)
    return ItemsPublic(data=items, count=len(items))
