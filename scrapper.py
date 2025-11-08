import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import csv

# ---------------- CONFIG ---------------- #
LINKEDIN_COOKIE = "li_at=YOUR LINKEDIN COOKIE WHICH YOU WILL GET IN DEVTOOLS->APPLICATION->STORAGE->COOKIES->li_at(Value)"


PROFILE_URLS = [
    "https://www.linkedin.com/in/satyanadella/",
    "https://www.linkedin.com/in/ravi-shankar-bejini-5887711b0/"
]
OUTPUT_CSV = "linkedin_profiles.csv"
# ---------------------------------------- #

async def scrape_and_parse(page, url, index):
    print(f"\n🌐 Visiting: {url}")
    await page.goto(url, timeout=60000)
    # Scroll to load dynamic content
    for _ in range(8):
        await page.mouse.wheel(0, 1500)
        await page.wait_for_timeout(1500)

    # Save raw HTML
    html = await page.content()
    dump_name = f"profile_{index+1}.html"
    with open(dump_name, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 Saved full HTML → {dump_name} ({len(html)} bytes)")

    # ---------- Parse data locally ---------- #
    soup = BeautifulSoup(html, "html.parser")
    profile = {"url": url}

    # Name (usually the first <h1> or first large <p>)
    name_tag = soup.find("h1")
    if not name_tag:
        name_tag = soup.find("p")
    profile["name"] = name_tag.get_text(strip=True) if name_tag else "N/A"

    # Headline (look for the first <p> after name)
    headline_tag = soup.find("p", string=lambda x: x and len(x.split()) > 2)
    profile["headline"] = headline_tag.get_text(strip=True) if headline_tag else "N/A"

    # Education
    edu_section = soup.find(string=lambda t: "Education" in t or "Educación" in t)
    education = []
    if edu_section:
        for p in soup.find_all("p"):
            txt = p.get_text(strip=True)
            if any(k in txt for k in ["University", "Institute", "School", "College"]):
                education.append(txt)
    profile["education"] = " | ".join(education) if education else "N/A"

    # Experience
    exp_section = soup.find(string=lambda t: "Experience" in t or "Experiencia" in t)
    experiences = []
    for p in soup.find_all("p"):
        txt = p.get_text(strip=True)
        if any(k in txt for k in ["CEO", "Founder", "Engineer", "Manager", "Developer", "Intern"]):
            experiences.append(txt)
    profile["experience"] = " | ".join(experiences) if experiences else "N/A"

    # Print nicely to console
    print("🧠 Extracted:")
    print(f"  👤 Name: {profile['name']}")
    print(f"  💼 Headline: {profile['headline']}")
    print(f"  🎓 Education: {profile['education']}")
    print(f"  🧾 Experience: {profile['experience']}")
    print("-" * 80)

    return profile

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context()
        # Add LinkedIn auth cookie
        await context.add_cookies([
            {
                "name": "li_at",
                "value": LINKEDIN_COOKIE.replace("li_at=", "").strip(),
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "httpOnly": True,
            }
        ])

        page = await context.new_page()
        results = []

        for i, url in enumerate(PROFILE_URLS):
            try:
                profile = await scrape_and_parse(page, url, i)
                results.append(profile)
            except Exception as e:
                print(f"❌ Failed to scrape {url}: {e}")

        # Write results to CSV
        keys = results[0].keys() if results else []
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n✅ Scraped {len(results)} profiles → {OUTPUT_CSV}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
