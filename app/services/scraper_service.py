"""
Scraper Orchestration Service.

This module provides the core ETL pipeline logic. It runs a given scraper,
passes the raw data through the normalization and deduplication layers,
and commits the final results to the database. It also maintains an audit log
of the scraper execution.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.opportunity import Opportunity
from app.database.models.scraper_run import ScraperRun
from app.scrapers.base import BaseScraper
from app.parsers.urls import canonicalize_url
from app.parsers.tagging import extract_deterministic_tags
from app.parsers.normalization import normalize_title, extract_deterministic_summary
from app.parsers.deduplication import find_existing_opportunity
from app.parsers.schemas import OpportunityCreate
from loguru import logger
from datetime import datetime, timezone

async def run_scraper_and_save(session: AsyncSession, scraper: BaseScraper):
    """
    Execute a scraper and save the normalized results to the database.

    Args:
        session (AsyncSession): The database session.
        scraper (BaseScraper): The scraper instance to run.

    Side Effects:
        - Creates a ScraperRun log entry (running status).
        - Fetches and parses data using the scraper.
        - Validates, normalizes, and deduplicates each record.
        - Inserts new Opportunities or updates existing ones.
        - Updates the ScraperRun log entry (success/failed status).
    """
    run_log = ScraperRun(
        source_name=scraper.source_name,
        started_at=datetime.now(timezone.utc),
        status="running"
    )
    session.add(run_log)
    await session.commit()
    await session.refresh(run_log)
    
    try:
        raw_results = await scraper.scrape()
        
        records_added = 0
        records_updated = 0
        
        for raw in raw_results:
            try:
                # 1. Validate with Pydantic
                opp_in = OpportunityCreate(**raw)
                
                # 2. Normalize fields
                canonical = canonicalize_url(str(opp_in.source_url))
                norm_title = normalize_title(opp_in.title)
                summary = extract_deterministic_summary(opp_in.description)
                tags = extract_deterministic_tags(opp_in.title + " " + (opp_in.description or ""))
                
                # 3. Deduplicate
                existing = await find_existing_opportunity(
                    session, canonical, norm_title, opp_in.organization
                )
                
                if existing:
                    # Update existing record fields with latest parsed data
                    existing.title = opp_in.title
                    existing.category = opp_in.category
                    existing.source_url = str(opp_in.source_url)
                    existing.description = opp_in.description
                    existing.summary = summary
                    existing.tags = tags
                    existing.deadline = opp_in.deadline
                    existing.event_start = opp_in.event_start
                    existing.event_end = opp_in.event_end
                    existing.scraped_at = datetime.now(timezone.utc)
                    existing.last_seen_at = datetime.now(timezone.utc)
                    existing.is_active = True
                    records_updated += 1
                else:
                    # Create new
                    new_opp = Opportunity(
                        title=opp_in.title,
                        normalized_title=norm_title,
                        organization=opp_in.organization,
                        category=opp_in.category,
                        source_name=opp_in.source_name,
                        source_url=str(opp_in.source_url),
                        canonical_url=canonical,
                        description=opp_in.description,
                        summary=summary,
                        tags=tags,
                        deadline=opp_in.deadline,
                        event_start=opp_in.event_start,
                        event_end=opp_in.event_end,
                        last_seen_at=datetime.now(timezone.utc),
                        scraped_at=datetime.now(timezone.utc)
                    )
                    session.add(new_opp)
                    records_added += 1
                    
            except Exception as e:
                logger.error(f"Error processing record in {scraper.source_name}: {e}")
                
        # Update run log
        run_log.status = "success"
        run_log.records_added = records_added
        run_log.records_updated = records_updated
        run_log.finished_at = datetime.now(timezone.utc)
        
        await session.commit()
        logger.info(f"Scraper {scraper.source_name} completed successfully. Added: {records_added}, Updated: {records_updated}")
        
    except Exception as e:
        logger.exception(f"Scraper {scraper.source_name} failed completely")
        run_log.status = "failed"
        run_log.error_message = str(e)
        run_log.finished_at = datetime.now(timezone.utc)
        await session.commit()
