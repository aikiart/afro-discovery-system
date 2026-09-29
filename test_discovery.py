from agents.discovery_agent import DiscoveryAgent

agent = DiscoveryAgent()

results = agent.discover()

for result in results:

    print(
        result["query"]
    )

    print(
        result["url"]
    )

    print()