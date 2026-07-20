

def metrics_calculator(requests: list):
    if not requests:
        return {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "success_rate": 0.0,
            "failure_rate": 0.0,
            "average_latency": None,
            "min_latency": None,
            "max_latency": None,
        }

    total_requests = len(requests)
    total_latency = 0
    successful_requests = 0

    max_latency = float("-inf")
    min_latency = float("inf")

    for request in requests:
        if request["success"]:
            successful_requests += 1

            latency = request["latency_ms"]
            total_latency += latency

            if latency > max_latency:
                max_latency = latency

            if latency < min_latency:
                min_latency = latency

    failed_requests = total_requests - successful_requests

    success_rate = round((successful_requests / total_requests) * 100, 2)
    failure_rate = round((failed_requests / total_requests) * 100, 2)

    if successful_requests > 0:
        average_latency = round(total_latency / successful_requests, 2)
    else:
        average_latency = None
        min_latency = None
        max_latency = None

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "success_rate": success_rate,
        "failure_rate": failure_rate,
        "average_latency": average_latency,
        "minimum_latency": min_latency,
        "maximum_latency": max_latency,
    }


if __name__=='__main__':
    requests = [
        {
            "status_code": 200,
            "latency_ms": 52.31,
            "success": True,
            "error": None,
        },
        {
            "status_code": 200,
            "latency_ms": 61.24,
            "success": True,
            "error": None,
        },
        {
            "status_code": None,
            "latency_ms": None,
            "success": False,
            "error": "Connection Timeout",
        },
    ]

    print(metrics_calculator(requests))