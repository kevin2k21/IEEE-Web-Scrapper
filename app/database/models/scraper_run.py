import uuid
from sqlalchemy import String, Integer, DateTime, text, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

from app.database.models.base import Base

class ScraperRun(Base):
    """
    SQLAlchemy model tracking the execution of a scraper.

    This model serves as an audit log to monitor the health, duration,
    and success rate of scraping jobs.

    Attributes:
        id (uuid.UUID): Primary key.
        source_name (str): The identifier of the scraper that was run.
        started_at (datetime): Timestamp when the run started.
        finished_at (Optional[datetime]): Timestamp when the run finished.
        status (str): Current status of the run ('running', 'success', 'failed').
        records_added (int): Number of new opportunities inserted during this run.
        records_updated (int): Number of existing opportunities updated during this run.
        error_message (Optional[str]): Exception details if the run failed.
        parser_version (Optional[str]): Version of the parser used (for tracking changes).
    """
    __tablename__ = "scraper_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    source_name: Mapped[str] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    records_added: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parser_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
