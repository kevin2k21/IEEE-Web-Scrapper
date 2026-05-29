"""
Background Job Scheduler Runner.

This module configures APScheduler to run the scrapers on a recurring schedule.
It groups all available scrapers and executes them sequentially.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.session import AsyncSessionLocal
from app.scrapers.ieee_students.opportunities import IeeeStudentsScraper
from app.scrapers.ieee_cs.cfp import IeeeCsCfpScraper
from app.scrapers.conferences.calendar import IeeeCsCalendarScraper
from app.scrapers.ieee.madras import IeeeMadrasScraper
from app.scrapers.conferences.top_events import IeeeCsTopEventsScraper
from app.scrapers.ieee.r10_sac import IeeeR10SacScraper
from app.scrapers.ieee_students.contests import IeeeStudentContestsScraper
from app.scrapers.ieee_cs.linkedin import IeeeCsLinkedinScraper
from app.scrapers.ieee.mas_linkedin import IeeeMasLinkedinScraper
from app.scrapers.ieee.r10_linkedin import IeeeR10LinkedinScraper
from app.services.scraper_service import run_scraper_and_save
from loguru import logger

scheduler = AsyncIOScheduler()

async def run_all_scrapers():
    """
    Execute all configured scrapers one by one.

    Creates a new database session, instantiates each scraper, and passes it
    to the scraper orchestration service. Logs progress sequentially.
    """
    logger.info("Starting scheduled job: Running all scrapers")
    async with AsyncSessionLocal() as session:
        # 1. Run IEEE Students Scraper
        logger.info("Scheduler: Running IEEE Students Scraper...")
        students_scraper = IeeeStudentsScraper()
        await run_scraper_and_save(session, students_scraper)
        
        # 2. Run IEEE CS CFP Scraper
        logger.info("Scheduler: Running IEEE Computer Society CFP Scraper...")
        cs_scraper = IeeeCsCfpScraper()
        await run_scraper_and_save(session, cs_scraper)
        
        # 3. Run IEEE CS Calendar Scraper
        logger.info("Scheduler: Running IEEE Computer Society Conference Calendar Scraper...")
        calendar_scraper = IeeeCsCalendarScraper()
        await run_scraper_and_save(session, calendar_scraper)
        
        # 4. Run IEEE Madras Section Scraper
        logger.info("Scheduler: Running IEEE Madras Section Scraper...")
        madras_scraper = IeeeMadrasScraper()
        await run_scraper_and_save(session, madras_scraper)
        
        # 5. Run IEEE CS Top Events Scraper
        logger.info("Scheduler: Running IEEE Computer Society Top Events Scraper...")
        top_events_scraper = IeeeCsTopEventsScraper()
        await run_scraper_and_save(session, top_events_scraper)
        
        # 6. Run IEEE Region 10 SAC Scraper
        logger.info("Scheduler: Running IEEE Region 10 SAC Scraper...")
        r10_scraper = IeeeR10SacScraper()
        await run_scraper_and_save(session, r10_scraper)
        
        # 7. Run IEEE Student Contests Scraper
        logger.info("Scheduler: Running IEEE Student Contests Scraper...")
        contests_scraper = IeeeStudentContestsScraper()
        await run_scraper_and_save(session, contests_scraper)
        
        # 8. Run IEEE CS LinkedIn Scraper
        logger.info("Scheduler: Running IEEE CS LinkedIn Scraper...")
        linkedin_scraper = IeeeCsLinkedinScraper()
        await run_scraper_and_save(session, linkedin_scraper)
        
        # 9. Run IEEE MAS LinkedIn Scraper
        logger.info("Scheduler: Running IEEE MAS LinkedIn Scraper...")
        mas_linkedin_scraper = IeeeMasLinkedinScraper()
        await run_scraper_and_save(session, mas_linkedin_scraper)
        
        # 10. Run IEEE R10 LinkedIn Scraper
        logger.info("Scheduler: Running IEEE R10 LinkedIn Scraper...")
        r10_linkedin_scraper = IeeeR10LinkedinScraper()
        await run_scraper_and_save(session, r10_linkedin_scraper)
        
    logger.info("Scheduled job: All scrapers completed successfully.")

def start_scheduler():
    scheduler.add_job(run_all_scrapers, "interval", hours=6)
    scheduler.start()
    logger.info("Scheduler started with interval 6 hours")
