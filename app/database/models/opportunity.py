import uuid
from sqlalchemy import String, Text, DateTime, Boolean, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

from app.database.models.base import Base

class Opportunity(Base):
    """
    SQLAlchemy model representing a scraped opportunity.

    This model stores all normalized information about an opportunity,
    including its title, organization, dates, tags, and tracking data
    for deduplication.

    Attributes:
        id (uuid.UUID): Primary key.
        title (str): Original title of the opportunity.
        normalized_title (str): Lowercase, stripped title for deduplication.
        organization (str): The organization offering the opportunity (e.g., 'IEEE').
        category (str): Type of opportunity (e.g., 'Scholarship', 'Conference').
        source_name (str): Identifier of the scraper that found this (e.g., 'ieee_cs_cfp').
        source_url (str): The original URL where this was scraped from.
        canonical_url (str): URL stripped of tracking parameters for deduplication.
        description (Optional[str]): Full description or raw HTML snippet.
        summary (Optional[str]): Extracted short summary.
        deadline (Optional[datetime]): Submission deadline, if any.
        event_start (Optional[datetime]): Event start date, if applicable.
        event_end (Optional[datetime]): Event end date, if applicable.
        tags (list): JSON array of tags categorizing the opportunity.
        is_active (bool): Whether the opportunity is still active on the source.
        last_seen_at (datetime): Timestamp when this was last observed.
        scraped_at (datetime): Timestamp of initial scrape.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.
    """
    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    normalized_title: Mapped[str] = mapped_column(String, nullable=False)
    organization: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    source_name: Mapped[str] = mapped_column(String, nullable=False)
    source_url: Mapped[str] = mapped_column(String, nullable=False)
    canonical_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    event_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    event_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    tags: Mapped[list] = mapped_column(JSONB, nullable=True, server_default='[]')
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()"), nullable=False)
