import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.session import AsyncSessionLocal
from app.database.models.opportunity import Opportunity
from sqlalchemy import select

async def main():
    print("Connecting to DB and querying opportunities...")
    async with AsyncSessionLocal() as session:
        stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
        result = await session.execute(stmt)
        opportunities = result.scalars().all()
        
    print(f"Total opportunities found: {len(opportunities)}")
    
    # Track unique categories
    categories = {}
    for opp in opportunities:
        categories[opp.category] = categories.get(opp.category, 0) + 1
        
    print("\nCategory Distribution:")
    for cat, count in categories.items():
        print(f" - {cat}: {count}")
        
    print("\nFirst 10 records sample:")
    for opp in opportunities[:10]:
        print(f"Title: {opp.title[:40]}... | Category: {opp.category} | Org: {opp.organization}")

if __name__ == "__main__":
    asyncio.run(main())
