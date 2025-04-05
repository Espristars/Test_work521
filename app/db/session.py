from sqlalchemy.ext.asyncio import create_async_engine
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from os import getenv

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=getenv("DATABASE_URL"),
    session_dependency_key="db_session",
    create_all=True,
)

plugin = SQLAlchemyPlugin(config=sqlalchemy_config)

engine = create_async_engine(sqlalchemy_config.connection_string, echo=True)
async_sessionmaker = sqlalchemy_config.session_maker
