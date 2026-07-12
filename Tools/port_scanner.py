import socket as sc


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

def get_service(port):
    try:
        return sc.getservbyport(port)
    except:
        return "Unknown"
    

def scan_ports(ip, port):
    for port in ports:
        service = get_service(port)

        if scan_port(ip, port):
            print(f"[+] port {port} OPEN ({service})")
        else:
            print(f"[-] port {port} CLOSED ({service})")



target = input("Enter your Target IP adrress: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter end port: "))

ports = range(start_port, end_port + 1)

scan_ports(target, ports)