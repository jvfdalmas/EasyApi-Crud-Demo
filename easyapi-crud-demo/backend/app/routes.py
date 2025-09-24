from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from .models import Item
from .schemas import ItemCreate, ItemRead


router = APIRouter(prefix="/items", tags=["items"])
"""Router exposing CRUD endpoints for `Item` resources."""


@router.get("/", response_model=List[ItemRead])
async def list_items(session: AsyncSession = Depends(get_session)) -> List[ItemRead]:
    """Return all items ordered by newest first."""
    result = await session.execute(select(Item).order_by(Item.id.desc()))
    items = result.scalars().all()
    return [ItemRead.model_validate(i) for i in items]


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: AsyncSession = Depends(get_session)) -> ItemRead:
    """Create a new item with the provided name."""
    item = Item(name=payload.name)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return ItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)) -> None:
    """Delete an item by id. Returns 404 if it does not exist."""
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await session.delete(item)
    await session.commit()
    return None


