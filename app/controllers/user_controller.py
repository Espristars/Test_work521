from litestar import Controller, post, get, patch, delete
from litestar.exceptions import NotFoundException
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.models.user_model import User
from sqlalchemy import select
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import msgspec

class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: UserCreate, db_session: AsyncSession) -> UserRead:
        user_data = msgspec.to_builtins(data)
        user = User(**user_data)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        user_data.pop("password", None)
        return UserRead(**user.to_dict(exclude={"password"}))

    @get()
    async def list_users(self, db_session: AsyncSession) -> List[UserRead]:
        result = await db_session.execute(select(User))
        users = result.scalars().all()
        return [UserRead(**user.to_dict(exclude={"password"})) for user in users]

    @get("/{user_id:uuid}")
    async def get_user(self, user_id: UUID, db_session: AsyncSession) -> UserRead:
        result = await db_session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NotFoundException("User not found")
        return UserRead(**user.to_dict(exclude={"password"}))

    @patch("/{user_id:uuid}")
    async def update_user(self, user_id: UUID, data: UserUpdate, db_session: AsyncSession) -> UserRead:
        result = await db_session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NotFoundException("User not found")
        for key, value in data.__dict__.items():
            if value is not None:
                setattr(user, key, value)
        await db_session.commit()
        await db_session.refresh(user)
        return UserRead(**user.to_dict(exclude={"password"}))

    @delete("/{user_id:uuid}", status_code=204)
    async def delete_user(self, user_id: UUID, db_session: AsyncSession) -> None:
        user = await db_session.get(User, user_id)
        if not user:
            raise NotFoundException("User not found")
        await db_session.delete(user)
        await db_session.commit()
