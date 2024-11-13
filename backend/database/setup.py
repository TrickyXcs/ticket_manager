from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import DbConfig


def create_engine(db: DbConfig, echo=False) -> AsyncEngine:
    return create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
        connect_args={'server_settings': {'options':'-c timezone=Europe/Kyiv'}}
    )



def create_session_pool(engine) -> async_sessionmaker[AsyncSession]:
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool