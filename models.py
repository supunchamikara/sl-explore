from datetime import datetime
from sqlalchemy import Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    attractions: Mapped[list["Attraction"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")


class Attraction(Base):
    __tablename__ = "attractions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    province: Mapped[str] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="attractions")
    images: Mapped[list["AttractionImage"]] = relationship(
        back_populates="attraction", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="attraction",
        cascade="all, delete-orphan",
        order_by="Comment.created_at",
    )


class AttractionImage(Base):
    __tablename__ = "attraction_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attraction_id: Mapped[int] = mapped_column(ForeignKey("attractions.id"))
    image_path: Mapped[str] = mapped_column(String(500))

    attraction: Mapped["Attraction"] = relationship(back_populates="images")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attraction_id: Mapped[int] = mapped_column(ForeignKey("attractions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    attraction: Mapped["Attraction"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")
