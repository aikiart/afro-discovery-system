from agents.discovery_agent import DiscoveryAgent

agent = DiscoveryAgent()

queries = [
    "African mobile apps",
    "African software platforms",
    "African educational websites",
    "African fintech apps",
    "African ecommerce platforms",
    "African health apps",
    "African media websites",
    "African technology startups",
    "Black owned mobile apps",
    "Black owned software companies",
    "Black owned ecommerce platforms",
    "Black educational organizations",
    "Afrocentric learning resources",
    "Afrocentric community platforms",
    "African cultural organizations",
    "African nonprofit organizations",
    "African professional networks",
    "African entrepreneur platforms",
    "African arts platforms",
    "African wellness platforms"
]

all_results = []

for query in queries:

    result = agent.search(query)

    all_results.append(result)

agent.save_results(all_results)

print(f"Completed {len(queries)} searches.")