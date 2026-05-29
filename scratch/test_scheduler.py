import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.scheduler.runner import start_scheduler, scheduler, run_all_scrapers
from loguru import logger

async def test_scheduler():
    logger.info("Initializing scheduler for verification test...")
    start_scheduler()
    
    # 1. Check if scheduler is running
    is_running = scheduler.running
    logger.info(f"Is scheduler running? {is_running}")
    
    # 2. Get list of scheduled jobs
    jobs = scheduler.get_jobs()
    logger.info(f"Total scheduled jobs: {len(jobs)}")
    for j in jobs:
         logger.info(f" - Job ID: {j.id} | Trigger: {j.trigger} | Next Run: {j.next_run_time}")
         
    # 3. Shutdown the scheduler so it doesn't run indefinitely in the test
    scheduler.shutdown()
    logger.info("Scheduler shutdown successfully after verification.")
    
    # 4. End-to-end dry-run of the scheduler job function
    logger.info("Running a single execution of the scheduled job function to ensure end-to-end correctness...")
    await run_all_scrapers()

if __name__ == "__main__":
    asyncio.run(test_scheduler())
