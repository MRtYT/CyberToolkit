import socket as sc
from concurrent.futures import ThreadPoolExecutor



def scan_port(ip, port):
    try:
        sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((ip, port))

        sock.close()

        return result == 0
    except Exception:
        return False

def get_service(port):
    try:
        return sc.getservbyport(port)
    except:
        return "Unknown"
    
def grab_banner(ip, port):
    try:
        sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sock.settimeout(2)

        sock.connect((ip, port))

        #HTTP
        if port in [80, 8080, 8000]:
            request = (
                f"GET / HTTP/1.1\r\n"
                f"HOST: {ip}\r\n"
                "connection: close\r\n\r\n"
            )
            sock.send(request.encode())

        #FTP AND SSH BANNER
        elif port in [21, 22]:
            pass
        
        #General
        else:
            sock.send(b"\r\n")

        banner = sock.recv(4096)

        sock.close()

        response = banner.decode(errors="ignore").strip()

        if port in [80,8080,8000]:
            return response.split("\r\n\r\n")[0]
             
        return response
    
    except Exception:
        return None

def scan_single(ip, port):
    #To scan a single port

    service = get_service(port)

    banner = None

    if scan_port(ip, port):
        banner = grab_banner(ip, port)

        return{
        "port": port,
        "status": "OPEN",
        "service": service,
        "banner": banner
        }

    return{
        "port": port,
        "status": "CLOSED",
        "service": service,
        "banner": banner
    }



def scan_ports(ip, ports, threads=50):
    
    results = []

    with ThreadPoolExecutor(max_workers=threads) as executor:

        scan_results = executor.map(
            lambda port: scan_single(ip, port),
            ports
        )

        for result in scan_results:
            results.append(result)

    return results
