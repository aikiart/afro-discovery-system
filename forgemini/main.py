from agents.discovery_agent import DiscoveryAgent

agent = DiscoveryAgent()

queries = agent.load_queries()

print("\nDiscovery Queries:\n")

for query in queries:
    print(query)