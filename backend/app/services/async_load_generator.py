import asyncio
import httpx
import time


async def async_call_generate(no_of_requests,url):
    async with httpx.AsyncClient() as client:
        task = [async_generate_request(client,url)
                    for _ in range(no_of_requests)
                ]
        start = time.perf_counter()
        results = await asyncio.gather(*task)
        end = time.perf_counter()

        duration = (end-start)*1000
        rps = no_of_requests/(duration/1000)

    return results,duration,rps
    

async def async_generate_request(client:httpx.AsyncClient,url: str):
    try:
        start = time.perf_counter()

        response = await client.get(url,timeout=15)

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