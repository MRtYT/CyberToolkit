import requests
from concurrent.futures import ThreadPoolExecutor

def check_subdomain(domain, subdomain):

    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=3, stream=True)
        return {
            "subdomain": f"{subdomain}.{domain}",
            "status": "FOUND",
            "status_code": response.status_code,
        }
    except Exception:
        # catch network and HTTP errors; treat as not found/unreachable
        return None
    
def scan_subdomains(domain, subdomain_list, threads= 40):

    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        scan_results = executor.map(
            lambda sub: check_subdomain(domain, sub), subdomain_list
        )

        for result in scan_results:
            if result:
                results.append(result)
    
    return results
