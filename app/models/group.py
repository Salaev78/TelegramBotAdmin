from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.database.base import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    members: Mapped[list["GroupMember"]] = relationship(
)
    back_populates="group",
    messages = relationship(
    "Message",
    back_populates="group",
    cascade="all, delete-orphan",

)