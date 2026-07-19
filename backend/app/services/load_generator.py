import requests
import time 


def generate_requests(tot_requests:int,url:str):
    result = []
    for i in range(tot_requests):
        try:
            start = time.perf_counter()
            response = requests.get(url,timeout=15)
            end = time.perf_counter()

            latency = (end - start) * 1000

            result.append({
                "status_code" : response.status_code,
                "latency_ms" : round(latency,2),
                "success" : response.ok,
                "error" : None
            })

        except Exception as e:
            result.append({
                "status_code" : None,
                "latency_ms" : None,
                "success" : None,
                "error" : e
            })

    return result

url = "https://jsonplaceholder.typicode.com/posts"
print(generate_requests(10,url))