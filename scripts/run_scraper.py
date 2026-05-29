import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

async def main():
    async with AsyncSessionLocal() as session:
        logger.info("Manually running IEEE Students Scraper...")
        students_scraper = IeeeStudentsScraper()
        await run_scraper_and_save(session, students_scraper)
        
        logger.info("Manually running IEEE Computer Society CFP Scraper...")
        cs_scraper = IeeeCsCfpScraper()
        await run_scraper_and_save(session, cs_scraper)
        
        logger.info("Manually running IEEE Computer Society Conference Calendar Scraper...")
        calendar_scraper = IeeeCsCalendarScraper()
        await run_scraper_and_save(session, calendar_scraper)
        
        logger.info("Manually running IEEE Madras Section Scraper...")
        madras_scraper = IeeeMadrasScraper()
        await run_scraper_and_save(session, madras_scraper)
        
        logger.info("Manually running IEEE Computer Society Top Events Scraper...")
        top_events_scraper = IeeeCsTopEventsScraper()
        await run_scraper_and_save(session, top_events_scraper)
        
        logger.info("Manually running IEEE Region 10 SAC Scraper...")
        r10_scraper = IeeeR10SacScraper()
        await run_scraper_and_save(session, r10_scraper)
        
        logger.info("Manually running IEEE Student Contests Scraper...")
        contests_scraper = IeeeStudentContestsScraper()
        await run_scraper_and_save(session, contests_scraper)
        
        logger.info("Manually running IEEE Computer Society LinkedIn Scraper...")
        linkedin_scraper = IeeeCsLinkedinScraper()
        await run_scraper_and_save(session, linkedin_scraper)
        
        logger.info("Manually running IEEE Madras Section LinkedIn Scraper...")
        mas_linkedin_scraper = IeeeMasLinkedinScraper()
        await run_scraper_and_save(session, mas_linkedin_scraper)
        
        logger.info("Manually running IEEE Region 10 LinkedIn Scraper...")
        r10_linkedin_scraper = IeeeR10LinkedinScraper()
        await run_scraper_and_save(session, r10_linkedin_scraper)
        
    logger.info("Done.")

if __name__ == "__main__":
    asyncio.run(main())
