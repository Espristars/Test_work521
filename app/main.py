from litestar import Litestar
from app.controllers.user_controller import UserController
from app.db.session import plugin
from alembic.config import Config
from alembic import command
import asyncio
import alembic

async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    await asyncio.get_event_loop().run_in_executor(
        None,
        alembic.command.upgrade,
        alembic_cfg,
        "head",
        False,
        None
    )


app = Litestar(
    on_startup=[run_migrations],
    route_handlers=[UserController],
    plugins=[plugin]
)