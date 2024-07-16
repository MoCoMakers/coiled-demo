import coiled

"""
Run a simple connection to a Coiled cluster.
"""

cluster = coiled.Cluster(
    n_workers=5,
    name="arxiv",
    package_sync=False, 
    backend_options={"region": "us-east1"},  # faster and cheaper
)
client = cluster.get_client()

def inc(x):
    return x + 1

future = client.submit(inc, 10)
result = future.result() # returns 11

print(result)
print("Closing cluster")
cluster.close()
