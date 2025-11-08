# 🚀 LinkedIn Profile Scraper (Assignment 1)

This project demonstrates a complete LinkedIn profile scraper built with **Python + Playwright** as part of the Aeroleads assignment.

It automates LinkedIn profile browsing, extracts useful profile information, and saves results into a CSV file.

---

## 🎯 Features
- Logs in using your `li_at` cookie (secure, no password required)
- Opens and scrolls through profile pages
- Dumps full HTML for verification
- Extracts:
  - 👤 Name  
  - 💼 Headline  
  - 🎓 Education  
  - 🧾 Experience
- Prints data live in the console  
- Saves everything to `linkedin_profiles.csv`

---

## ⚙️ Tech Stack
| Layer | Tool |
|-------|------|
| Automation | [Playwright](https://playwright.dev/python/) |
| Parsing | [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) |
| Language | Python 3.9+ |
| Output | CSV + HTML dumps |

---

## 🧩 Setup

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
playwright install
