"""
Deduplication logic for scraped opportunities.

This module provides functions to check if a newly scraped opportunity
already exists in the database to prevent duplicate entries.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from app.database.models.opportunity import Opportunity
from typing import Optional

async def find_existing_opportunity(
    session: AsyncSession, 
    canonical_url: str, 
    normalized_title: str, 
    organization: str
) -> Optional[Opportunity]:
    """
    Find if an opportunity already exists using deterministic rules.

    Checks the database for an existing opportunity that matches either:
    1. The exact canonical URL.
    2. The combination of normalized title and organization name.

    Args:
        session (AsyncSession): The database session.
        canonical_url (str): The URL stripped of tracking parameters.
        normalized_title (str): The cleaned, lowercase title.
        organization (str): The organization name.

    Returns:
        Optional[Opportunity]: The existing Opportunity object if found, else None.
    """
    
    stmt = select(Opportunity).where(
        or_(
            Opportunity.canonical_url == canonical_url,
            and_(
                Opportunity.normalized_title == normalized_title,
                Opportunity.organization == organization
            )
        )
    ).limit(1)
    
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
