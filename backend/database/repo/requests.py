from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

# from backend.database.setup import create_engine


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession



# if __name__ == "__main__":
#     from backend.database.setup import create_session_pool
#     from config import Config

#     async def example_usage(config: Config):
#         """
#         Example usage function for the RequestsRepo class.
#         Use this function as a guide to understand how to utilize RequestsRepo for managing user data.
#         Pass the config object to this function for initializing the database resources.
#         :param config: The config object loaded from your configuration.
#         """
#         engine = create_engine(config.db)
#         session_pool = create_session_pool(engine)

#         async with session_pool() as session:
#             repo = RequestsRepo(session)

#             # Replace user details with the actual values
#             user = await repo.users.get_by_email(email="test@gmail.com")