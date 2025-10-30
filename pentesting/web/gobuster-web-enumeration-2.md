GOBUSTER - Web Enumeration

Flag	Long Flag	Description
-t	--threads	Number of concurrent threads (default 10)
-v	--verbose	Verbose output
-z	--no-progress	Don't display progress
-q	--quiet	Don't print the banner and other noise
-o	--output	Output file to write results to
-u URL
-w WORD LIST

-c	--cookies	Cookies to use for requests
-x	--extensions	File extension(s) to search for
-H	--headers	Specify HTTP headers, -H 'Header1: val1' -H 'Header2: val2'
-k	--no-tls-validation	Skip TLS certificate verification
-n	--no-status	Don't print status codes
-P	--password	Password for Basic Auth
-s	--status-codes	Positive status codes
-b	--status-codes-blacklist	Negative status codes
-U	--username	Username for Basic Auth

dns

-c	--show-cname	Show CNAME Records (cannot be used with '-i' option)
-i	--show-ips	Show IP Addresses
-r	--resolver	Use custom DNS server (format server.com or server.com:port)

https://github.com/OJ/gobuster#dir-mode-options


    /usr/share/wordlists/dirbuster/directory-list-2.3-*.txt
    /usr/share/wordlists/dirbuster/directory-list-1.0.txt
    /usr/share/wordlists/dirb/big.txt
    /usr/share/wordlists/dirb/common.txt
    /usr/share/wordlists/dirb/small.txt
    /usr/share/wordlists/dirb/extensions_common.txt - Useful for when fuzzing for files!


Non-Standard Lists

             sudo apt install seclists

GOBUSTER PARA VHOST

    gobuster vhost -u http://webenum.thm -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt