import requests
import time 

start = time.perf_counter()
response = requests.get("https://jsonplaceholder.typicode.com/posts")
end = time.perf_counter()

latency = end - start 
print(f"Status Code : {response.status_code}")
print(f"Latency :{latency*1000:.2f} ms")