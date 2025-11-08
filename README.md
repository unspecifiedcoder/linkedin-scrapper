# LinkedIn Scraper
This script logs into LinkedIn using Playwright and scrapes user data (name, headline, education, experience) from profile URLs.
It saves data to CSV and dumps full HTML locally for verification.

### How to run
- Install dependencies:
  pip install playwright beautifulsoup4
  playwright install
- Add your LinkedIn li_at cookie in the script
- Run:
  python linkedin_scraper_final.py
- Output: linkedin_profiles.csv + HTML dumps

### Technologies
- Playwright (browser automation)
- BeautifulSoup (HTML parsing)
- CSV for structured output
