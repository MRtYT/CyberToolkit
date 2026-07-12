from tools.port_scanner import scan_ports
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

    target = input("\nTarget IP: ")

    start = int(input("Start port: "))
    end = int(input("End port: "))

    ports = range(start, end + 1)

    print("\nscanning...\n")

    results = scan_ports(target, ports)

    for result in results:
        if result["status"] == "OPEN":
            print(
                f"[+] {result['port']} OPEN"
                f"({result['service']})"
            )

            if result["banner"]:
                print(
                    f"      banner: {result['banner']}"
                )
        else:
            print(
                f"[-] {result['port']} CLOSED"
                f"({result['service']})"
            )


def pause():
    input("\nPress Enter to continue...")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    while True:
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
            print(colorama.Fore.RED + "coming soon...")
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