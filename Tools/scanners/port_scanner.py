import socket as sc
from concurrent.futures import ThreadPoolExecutor





def get_service(port):
    try:
        return sc.getservbyport(port)
    except Exception:
        return "Unknown"
    
def check_and_grab(ip, port):
    
    sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    sock.settimeout(2)

    try:
        

        sock.connect((ip, port))

        banner = None

        #HTTP
        if port in [80, 8080, 8000]:
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                "Connection: close\r\n\r\n"
            )
            sock.send(request.encode())
        #FTP AND SSH BANNER
        elif port in [21, 22]:
            pass
        #General
        else:
            sock.send(b"\r\n")
        try:

            ready_data = sock.recv(4096)
            response = banner.decode(errors="ignore").strip()

            if port in [80,8080,8000]:
                return response.split("\r\n\r\n")[0].split("\r\n")[0]
            else:
                banner = response if response else None
        except Exception:
            banner = None

        return {
            "port": port,
            "status": "OPEN",
            "service": get_service(port),
            "banner": banner
        }
    
    except (sc.timeout, ConnectionRefusedError, OSError):
        return {
            "port": port,
            "status": "CLOSED",
            "service": get_service(port),
            "banner": None
        }
    finally:
        sock.close()


def scan_ports(ip, ports, threads=50):
    
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:

        scan_results = executor.map(
            lambda port: check_and_grab(ip, port),
            ports
        )

        for result in scan_results:
            results.append(result)

    return results
