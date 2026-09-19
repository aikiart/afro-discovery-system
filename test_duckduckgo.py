from duckduckgo_search import DDGS

results = list(
    DDGS().text(
        "African fintech companies",
        max_results=10
    )
)

print("Results found:", len(results))

for result in results:
    print(result)