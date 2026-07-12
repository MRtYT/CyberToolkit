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
    

def scan_ports(ip, ports):
    for port in ports:
        service = get_service(port)

        if scan_port(ip, port):
            print(f"[+] port {port} OPEN ({service})")

            banner = grab_banner(ip, port)

            if banner:
                print("     Banner: ")
                print(f"    {banner}")
        else:
            print(f"[-] port {port} CLOSED ({service})")

def grab_banner(ip, port):
    try:
        sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sock.settimeout(3)

        sock.connect((ip, port))

        #HTTP
        if port in [80, 8080, 8000]:
            request = f"GET / HTTP/1.1\r\nHOST: {ip}\r\nconnection: close\r\n\r\n"
            sock.send(request.encode())

        #FTP BANNER
        elif port in [21, 22]:
            pass
        
        #General
        else:
            sock.send(b"\r\n")

        banner = sock.recv(4096)

        sock.close()

        response = banner.decode(errors="ignore")

        if port in [80,8080,8000]:
            return response.split("\r\n\r\n")[0]
             
        return response.strip()
    
    except Exception:
        return None


target = input("Enter your Target IP address: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter end port: "))

ports = range(start_port, end_port + 1)

scan_ports(target, ports)