import asyncio
import httpx
import time


async def async_call_generate(no_of_requests,url,concurrency):
    async with httpx.AsyncClient(timeout=15) as client:
        semaphore = asyncio.Semaphore(concurrency)
        task = [async_generate_request(client,url,semaphore)
                    for _ in range(no_of_requests)
                ]
        start = time.perf_counter()
        results = await asyncio.gather(*task)
        end = time.perf_counter()

        duration = (end-start)*1000
        rps = no_of_requests/(duration/1000)

    return results,duration,rps
    

async def async_generate_request(client:httpx.AsyncClient,url: str,semaphore):
    try:
        async with semaphore:
            start = time.perf_counter()
            response = await client.get(url)
            end = time.perf_counter()

        latency = (end - start) * 1000

        return {
            "status_code": response.status_code,
            "latency_ms": round(latency, 2),
            "success": response.is_success,
            "error": None
        }
    
    except Exception as e:
        return{
            "status_code": None,
            "latency_ms": None,
            "success": False,
            "error": str(e)
        }
