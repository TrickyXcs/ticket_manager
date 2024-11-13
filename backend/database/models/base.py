from datetime import datetime

from sqlalchemy import text, Uuid, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import registry
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated
from sqlalchemy_continuum import make_versioned


make_versioned(user_cls=None)

convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s", # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}

int_pk = Annotated[int, mapped_column(primary_key=True)]
uuid_pk = Annotated[Uuid, mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))]#)default=lambda: str(uuid4()))]

mapper_registry = registry(metadata=MetaData(naming_convention=convention))


class Base(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now())
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
