"""
FastAPI routes for Opportunity resources.

Provides endpoints to query, filter, and paginate through scraped opportunities.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
import uuid

from app.database.session import get_db
from app.database.models.opportunity import Opportunity

router = APIRouter()

@router.get("/")
async def list_opportunities(
    session: AsyncSession = Depends(get_db),
    category: Optional[str] = Query(None, description="Filter by opportunity category (e.g. 'Scholarship')"),
    organization: Optional[str] = Query(None, description="Filter by organization name (e.g. 'IEEE Computer Society')"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return (max 100)"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    List opportunities with optional filtering and pagination.

    Returns a list of active opportunities sorted by creation date (newest first).
    """
    stmt = select(Opportunity).where(Opportunity.is_active.is_(True))
    
    if category:
        stmt = stmt.where(Opportunity.category == category)
    if organization:
        stmt = stmt.where(Opportunity.organization == organization)
        
    stmt = stmt.order_by(desc(Opportunity.created_at)).limit(limit).offset(offset)
    
    result = await session.execute(stmt)
    opps = result.scalars().all()
    
    return [opp for opp in opps]

@router.get("/{id}")
async def get_opportunity(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    stmt = select(Opportunity).where(Opportunity.id == id)
    result = await session.execute(stmt)
    opp = result.scalar_one_or_none()
    
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    return opp
