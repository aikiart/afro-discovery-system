from agents.discovery_agent import DiscoveryAgent

agent = DiscoveryAgent()

results = agent.search(
    "African fintech apps"
)

agent.save_results(results)

print(
    f"Found {len(results)} results."
)