import socket as sc

services = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    135: "MSRPC",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB"
}


def scan_port(ip, port):
    try:
        sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sock.settimeout(3)

        result = sock.connect_ex((ip, port))

        sock.close()


        if result == 0:
            return True
        else:
            return False
    except Exception:
        return False
    
def scan_ports(ip, port):
    for port in ports:
        service = services.get(port, "Unknown")

        if scan_port(ip, port):
            print(f"[+] port {port} OPEN ({service})")
        else:
            print(f"[-] port {port} CLOSED ({service})")


target = input("Enter your Target IP adrress: ")

ports = [21, 22 ,80 ,135, 139, 443, 445]

scan_ports(target, ports)