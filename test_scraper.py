from agents.scraper_agent import ScraperAgent

agent = ScraperAgent()

result = agent.scrape(
    "https://www.microsoft.com"
)

print(result)