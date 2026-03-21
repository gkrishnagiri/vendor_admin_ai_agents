from retriever import search

query = "how to fix docker issue"

results = search(query)

for r in results:
    print("\n---\n", r[:300])