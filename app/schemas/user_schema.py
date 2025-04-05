from msgspec import Struct
import datetime
from typing import Optional

class UserCreate(Struct):
    name: str
    surname: str
    password: str

class UserUpdate(Struct, omit_defaults=True):
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

class UserRead(Struct):
    id: str
    name: str
    surname: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
