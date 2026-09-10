from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB


config: Mapped[dict] = mapped_column(JSONB)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))

class WidgetPreference(Base):
    __tablename__ = "widget_preferences"

    __table_args__ = (UniqueConstraint("user_id", "widget_name", name="uq_user_widget"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    widget_name: Mapped[str] = mapped_column(String(50))
    config: Mapped[dict] = mapped_column(JSONB)