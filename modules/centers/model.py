from datetime import datetime, timezone
from sqlalchemy import  Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid, JSON
from uuid import uuid4, UUID
from database import Base


class Center(Base):
    __tablename__ = 'centers'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    value: Mapped[list[list[float]]] = mapped_column(JSON, nullable=False)
    k: Mapped[int] = mapped_column(Integer, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(db_uuid, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    centers_chat: Mapped['Chat'] = relationship(
        'Chat',
        foreign_keys=[chat_id],
        back_populates='centers',
        lazy='noload'
    )