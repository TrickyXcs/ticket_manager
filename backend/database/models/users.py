
# ruff: noqa: F821

from sqlalchemy import sql
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from .base import int_pk, Base, TableNameMixin, TimestampMixin
import bcrypt
    

class User(Base, TableNameMixin, TimestampMixin):

    id: Mapped[int_pk]
    email: Mapped[str | None]
    hashed_password: Mapped[bytes | None]
    is_active: Mapped[bool | None] = mapped_column(server_default=sql.true())
    full_name: Mapped[str]
    telegram_id: Mapped[str]
    phone_number: Mapped[str | None]
    telegram_username: Mapped[str | None]

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self.hashed_password

    @password.setter
    def password(self, password: str):
        self.hashed_password = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
    
    def validate_password(self, password: str):
        return bcrypt.checkpw(str(password).encode(), self.hashed_password)

    @property
    def check_active(self) -> bool:
        return self.is_active
    
    @property
    def check_verificate(self) -> bool:
        return self.is_verificated
    
    def __str__(self):
        if self.username:
            return self.full_name
        return f"{self.telegram_id}"