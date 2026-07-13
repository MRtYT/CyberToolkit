from tools.scanners.port_scanner import scan_ports
from tools.scanners.subdomain_scanner import scan_subdomains
import os
import colorama

colorama.init(autoreset=True)


Banner = r"""
-- .·:'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.
-- : :    ██████╗██╗   ██╗██████╗ ███████╗██████╗ ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗   : :
-- : :   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝   : :
-- : :   ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝   ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║      : :
-- : :   ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║      : :
-- : :   ╚██████╗   ██║   ██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║      : :
-- : :    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      : :
-- '·:......................................................................................................:·'

"""

def port_scanner_menu():

    target = input("\nTarget IP / Domain: ")

    start = int(input("Start port: "))
    end = int(input("End port: "))

    ports = range(start, end + 1)

    print(colorama.Fore.YELLOW + f"\n[*]Starting scan on target: {target}")
    print(colorama.Fore.YELLOW + f"[*] Scanning {len(ports)} ports using 50 threads...\n")
    print(colorama.Fore.CYAN + "=" * 60)

    print(colorama.Fore.CYAN + f"{'PORT':<10}{'STATUS':<10}{"SERVICE":<15}{"BANNER"}")
    print(colorama.Fore.CYAN + "=" * 60)


    results = scan_ports(target, ports)

    open_count = 0
    closed_count = 0

    for result in results:
        if result["status"] == "OPEN":
            open_count += 1

            banner_text = result["banner"] if result["banner"] else "-"

            print(colorama.Fore.GREEN + f"{result['port']:<10}{result['status']:<10}{result['service']:<15}{banner_text}")
        
        else:
            closed_count += 1

    print(colorama.Fore.CYAN + "=" * 60)
    print(colorama.Fore.LIGHTBLUE_EX + f"[i] Scan finished. Found {open_count} open ports and {closed_count} closed ports.")



def subdomain_scanner_menu():

    domain = input("\nEnter Target Domain: ").strip()

    default_wordlist = [
        "www", "mail", "ftp", "admin", "blog", "dev", "test", "secure", 
        "webmail", "shop", "cpanel", "ns1", "ns2", "api", "staging", 
        "server", "vpn", "cloud", "support", "autodiscover"
    ]

    print(colorama.Fore.YELLOW + f"\n[*] Starting subdomain brute-force on: {domain}")
    print(colorama.Fore.YELLOW + f"[*] Testing {len(default_wordlist)} common subdomains using 40 threads...")
    print(colorama.Fore.CYAN + "=" * 50)
    print(colorama.Fore.CYAN + f"{'SUBDOMAIN':<30}{'STATUS':<10}{'CODE'}")
    print(colorama.Fore.CYAN + "=" * 50)

    results = scan_subdomains(domain, default_wordlist)

    for res in results:
        print(colorama.Fore.GREEN + f"{res['subdomain']:<30}{res['status']:<10}{res['status_code']}")

    print(colorama.Fore.CYAN + "=" * 50)
    print(colorama.Fore.LIGHTBLUE_EX + f"[i] Scan Finished. Found {len(results)} active subdomain") 



def pause():
    input("\nPress Enter to continue...")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    while True:
        clear()
        print(colorama.Fore.CYAN + Banner)
        print("""
[1] Port Scanner
[2] Subdomain Scanner
[3] Hash Tool
[4] Exit
""")
        
        choice = input(colorama.Fore.YELLOW + "cyberToolkit > ")

        if choice == "1":
            port_scanner_menu()
            pause()
        elif choice == "2":
            subdomain_scanner_menu()
            pause()
        elif choice == "3":
            print(colorama.Fore.RED + "coming soon...")
            pause()
        elif choice == "4":
            print(colorama.Fore.GREEN + "See you Soon!")
            pause()
            break

        else:
            print("invalid option")


if __name__ == "__main__":
    menu()