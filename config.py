from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from environs import Env

@dataclass
class Bot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS", subcast=int)
        use_redis = env.bool("USE_REDIS")
        return Bot(token=token, admin_ids=admin_ids, use_redis=use_redis)

@dataclass
class DbConfig:

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    #For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:

        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f'postgresql+{driver}',
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):

        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host, port=port, password=password, database=database, user=user
        )
    

@dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"
    
    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )
    
@dataclass
class Config:
    bot: Bot
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None

def load_config(path: str = None) -> Config:
    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot.from_env(env),
        db=DbConfig.from_env(env),
        redis=RedisConfig.from_env(env)
    )