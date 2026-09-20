from agents.scraper_agent import ScraperAgent

agent = ScraperAgent()

result = agent.scrape(
    "https://flutterwave.com"
)

print(result)