from agents.scraper_agent import ScraperAgent

agent = ScraperAgent()

result = agent.scrape(
    "https://african.business"
)

print(result)