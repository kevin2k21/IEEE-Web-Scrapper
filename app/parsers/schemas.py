from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class OpportunityCreate(BaseModel):
    """
    Pydantic schema for validating a raw opportunity before insertion.

    This schema ensures that all required fields are present and correctly typed
    before they are passed to the normalization and deduplication layers.

    Attributes:
        title (str): The title of the opportunity.
        organization (str): The organization providing the opportunity.
        category (str): The opportunity type.
        source_name (str): Identifier of the scraper.
        source_url (HttpUrl): The original URL (must be a valid URL).
        description (Optional[str]): Raw or lightly cleaned description.
        deadline (Optional[datetime]): The deadline, if available.
        event_start (Optional[datetime]): The event start date, if available.
        event_end (Optional[datetime]): The event end date, if available.
    """
    title: str
    organization: str
    category: str
    source_name: str
    source_url: HttpUrl
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    event_start: Optional[datetime] = None
    event_end: Optional[datetime] = None
