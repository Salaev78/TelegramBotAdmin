from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(255),
    )

    is_bot: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    group_members: Mapped[list["GroupMember"]] = relationship(
    back_populates="user",
    
    )
    
    messages = relationship(
    "Message",
    back_populates="user",
    cascade="all, delete-orphan",
    
    )