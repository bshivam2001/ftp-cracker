# FTP Cracker
A python script to automate cracking FTP Servers using dictionary attack

- Port Scanning
- Determine if a FTP Server is running and vulnerable
- Crack FTP servers with multi-threading support
- Minimal Requirements

## Prerequisites
1. Python 3 - project tested on Python 3.9, but generally should work well on any version of Python 3
2. An FTP Server - Can be a remote server, or locally hosted using an FTP Server software such as *FileZilla FTP Server*
3. A username that you'd like the program to try to crack
4. *[Optional]* A wordlist with passwords you'd like to try - one such wordlist is already included

## How to run
1. Install the requirements using pip - either using the requirements file, or install packages 'colorama' and 'playsound' separately  
```pip install -r requirements.txt```
2. Run ftp-cracker.py using command-line or your python IDE using the following flags  
    - You need to specify the target host's IP address at this point. You may optionally choose to specify the *username* and *wordlist* using the flags **-u** and **-p** respectively.  
    - You may use the **-i** flag to switch to interactive mode, where the program will prompt you to enter the username and wordlist 
    - The **-t** flag can be optionally used to specify the number of threads you would like the program to use
3. In the program menu,
      - Enter 1 to scan for open ports, or
      - Enter 2 to start the dictionary attack

Example command: `python ftp-cracker 127.0.0.1 -u admin -p wordlist.txt`  
where *127.0.0.1* is the FTP Server's IP, *admin* is the username to crack, and *wordlist.txt* is the dictionary word list
