PRD — IEEE / IEEE Computer Society Opportunity Intelligence System
1. Product Overview
Product Name

IEEE Opportunity Intelligence System
(MVP working name)

Problem Statement

UG/PG students miss valuable IEEE opportunities because information is scattered across multiple IEEE, IEEE Computer Society, conference, and regional websites.

Current problems:

No centralized discovery platform
Deadlines are difficult to track
IEEE websites are cluttered and inconsistent
Students cannot filter opportunities relevant to them
Important opportunities disappear quickly
Vision

Build a centralized opportunity intelligence platform that continuously discovers, classifies, stores, and exposes IEEE-related student opportunities in a structured and searchable format.

This is not just a scraper.

This is:

A structured discovery and intelligence platform for student opportunities.

2. Goals
Primary Goals
Automatically scrape IEEE/IEEE CS opportunities
Normalize messy data into structured objects
Store opportunities in PostgreSQL
Prevent duplicates
Enable filtering/searching
Run on a schedule automatically
Secondary Goals
AI-generated summaries
Tag extraction
Personalized recommendations
Deadline notifications
Semantic search
3. Target Users
Primary Users
Undergraduate students
Postgraduate students
Research students
IEEE student members
Secondary Users
IEEE student branches
Faculty coordinators
Research clubs
4. Scope
In Scope (MVP)
Opportunity Categories

Priority categories:

Priority	Category
P0	Scholarships
P0	Research Grants
P0	Conferences
P0	Call for Papers
P0	Competitions
P0	Hackathons
P0	Internships
P0	Fellowships
P1	Workshops
P1	Webinars
P1	Mentorship Programs
P1	Leadership Programs
P2	Certifications
Out of Scope (Initial MVP)

Do NOT scrape:

Generic IEEE news
Corporate advertisements
Professional-only opportunities
K-12 programs
Archived/dead opportunities
Entire IEEE article repositories
5. Core Features
5.1 Scheduled Scraping System
Description

System periodically scrapes predefined IEEE-related sources.

Requirements
Support static and JS-rendered pages
Configurable schedules
Incremental updates
Retry handling
Logging
Sources
IEEE official pages
IEEE CS pages
IEEE India pages
IEEE Region 10 pages
CFP pages
Conference pages
RSS feeds
5.2 Opportunity Normalization
Description

All scraped content must become one unified structured object.

Final Opportunity Schema
class Opportunity:
    id: UUID

    title: str
    organization: str
    opportunity_type: str

    summary: str
    description: str

    eligibility: dict
    tags: list[str]

    deadline: datetime
    event_date: datetime

    funding_amount: str
    benefits: list[str]

    application_link: str
    source_url: str

    location_scope: str

    posted_date: datetime

    scraped_at: datetime
    updated_at: datetime

    hash: str
6. Opportunity Data Model
Core Fields
Field	Required	Description
title	Yes	Opportunity title
organization	Yes	IEEE org/source
opportunity_type	Yes	Scholarship, CFP, etc
source_url	Yes	Original source
application_link	Yes	CTA/application page
deadline	Yes	Submission deadline
summary	Yes	AI-generated short summary
scraped_at	Yes	Scrape timestamp
hash	Yes	Deduplication hash
Eligibility Structure
{
  "education_level": ["UG", "PG"],
  "branches": ["CSE", "ECE"],
  "membership_required": true,
  "region_restriction": "India",
  "year_restriction": "2nd year+",
  "minimum_cgpa": "7.5"
}
Benefits Structure
[
  "Travel grant",
  "Publication opportunity",
  "Certificate",
  "Mentorship access"
]
Tags Example
[
  "AI/ML",
  "research",
  "india",
  "undergraduate",
  "funded"
]
7. System Architecture
                 ┌────────────────────┐
                 │ Scheduled Jobs     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Scraper Layer      │
                 │ requests/BS4       │
                 │ Playwright         │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Normalization      │
                 │ Cleaning           │
                 │ Classification     │
                 │ Deduplication      │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ PostgreSQL         │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ FastAPI Backend    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Frontend / Alerts  │
                 └────────────────────┘
8. Tech Stack
Layer	Technology
Scraping	BeautifulSoup + requests
JS Scraping	Playwright
Backend	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Validation	Pydantic
Scheduling	APScheduler
Deployment	Docker
Future Queue	Celery/RQ
9. Scraping Strategy
Static Pages

Use:

requests
BeautifulSoup
Typical Flow
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
Dynamic Pages

Use Playwright when:

JS-rendered content
Infinite scroll
API-driven pages
Delayed rendering
10. Database Design
Main Tables
opportunities

Stores normalized opportunities.

scrape_sources

Stores source configuration.

scrape_logs

Stores scraper execution logs.

tags

Stores reusable tags.

opportunity_tags

Many-to-many relationship.

11. Deduplication Strategy
Goal

Avoid repeated opportunities during scheduled scraping.

Method

Generate SHA256 hash using:

title + organization + source_url
Example
hashlib.sha256(unique_string.encode()).hexdigest()

Database constraint:

UNIQUE(hash)
12. Classification System
Opportunity Types

Supported categories:

Scholarship
Research Grant
Conference
CFP
Competition
Internship
Fellowship
Hackathon
Workshop
Webinar
Travel Grant
Mentorship
Certification
13. AI Features (Post-MVP)
AI Summary Generation

Example:

Input:

Large IEEE conference description.

Output:

“AI/ML-focused student conference with publication opportunities and travel grants.”

Tag Extraction

Example:

[
  "robotics",
  "research",
  "funded"
]
Eligibility Structuring

Convert messy paragraphs into structured eligibility objects.

14. API Requirements
Endpoints
GET /opportunities

Filters:

tags
type
deadline
region
eligibility
GET /opportunities/{id}

Single opportunity details.

GET /search

Keyword search.

GET /deadlines/upcoming

Upcoming deadlines.

15. Scheduling Requirements
Frequency
Source Type	Frequency
CFP pages	Every 6 hours
Scholarships	Daily
Conferences	Daily
RSS feeds	Every 2 hours
APScheduler Jobs
scheduler.add_job(
    scrape_ieee,
    trigger="interval",
    hours=6
)
16. Error Handling

System must handle:

HTML changes
Missing fields
Timeouts
HTTP failures
JS rendering failures
Duplicate entries
17. Logging Requirements

Track:

Scrape success/failure
Number of opportunities scraped
Number of duplicates skipped
Parsing failures
Response times
18. Non-Functional Requirements
Requirement	Target
Reliability	95% successful scrape runs
Scalability	10k+ opportunities
Maintainability	Modular scraper architecture
Performance	API <500ms avg
Extensibility	Easy addition of new sources
19. Folder Structure
project/
│
├── api/
│   ├── routes/
│   └── main.py
│
├── scrapers/
│   ├── ieee/
│   ├── conferences/
│   └── shared/
│
├── parsers/
│   ├── normalization.py
│   ├── classifiers.py
│   └── deduplication.py
│
├── database/
│   ├── models.py
│   ├── session.py
│   └── migrations/
│
├── scheduler/
│   └── jobs.py
│
├── services/
│   ├── summarization.py
│   ├── tagging.py
│   └── notifications.py
│
├── logs/
│
├── tests/
│
└── docker/
20. MVP Deliverables
MVP Must Include
Scraping
Multi-source scraping
Static + JS support
Data
PostgreSQL storage
Deduplication
Normalized schema
Backend
FastAPI endpoints
Filtering/search
Automation
APScheduler integration
AI
Basic summaries
Basic tags
21. Future Roadmap
V2
User accounts
Personalized feeds
Email alerts
Bookmarking
V3
Recommendation engine
Semantic search
AI ranking system
V4
Autonomous opportunity discovery agents
Cross-platform scraping
Discord/Telegram bots
22. Success Metrics
Technical Metrics
Scrape success rate
Duplicate reduction rate
Average scrape duration
API latency
Product Metrics
Opportunities discovered/week
Active users
Click-through rate
Deadline alert engagement
23. Key Engineering Principles
Principles
Deterministic > autonomous
Reliability > complexity
Clean data > flashy AI
Modular architecture
Source-specific scrapers
Strong normalization layer
24. Final Product Definition

This product is:

A continuously updating IEEE opportunity intelligence platform for students.

The scraper is infrastructure.

The actual value comes from:

discoverability
organization
filtering
relevance
deadlines
structured intelligence

Relevant implementation notes from your earlier planning are captured here.