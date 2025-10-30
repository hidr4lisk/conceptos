Front:

What are essential Linux commands and techniques for enumeration after gaining access to a system, and what key information do they provide?

Back:

1. **hostname**
   - Returns the system's hostname.
   - Can indicate system role in network (e.g., SQL-PROD-01).

2. **uname -a**
   - Displays kernel and system info.
   - Useful to identify kernel version for exploit search.

3. **/proc/version**
   - Shows kernel version and compiler info (e.g. GCC installed).

4. **/etc/issue**
   - Contains OS info (can be customized).

5. **ps**
   - Lists running processes.
   - Options:
     - `ps` (current shell)
     - `ps -A` (all processes)
     - `ps axjf` (process tree)
     - `ps aux` (all users, user info, detached processes)

6. **env**
   - Shows environment variables.
   - Check PATH for compilers or scripting languages useful for privilege escalation.

7. **sudo -l**
   - Lists commands current user can run with sudo.

8. **ls -la**
   - Lists all files including hidden and permissions.
   - Crucial for spotting hidden files or privilege escalation vectors.

9. **id**
   - Shows current user UID, GID, and group memberships.
   - Can query other users with `id username`.

10. **/etc/passwd**
    - Lists all system users.
    - Real users often have home directories under `/home`.
    - Podemos cortar con `cat /etc/passwd | cut -d ":" -f 1`, esto da la lista completa
    - También podemos usar `cat /etc/passwd | grep home`para tener solo USUARIOS

11. **history**
    - Displays command history.
    - May reveal useful info like usernames or passwords.

12. **ifconfig**
    - Lists network interfaces and IP info.
    - Useful for pivoting or understanding network topology.

13. **ip route**
    - Shows network routing table.

14. **netstat**
    - Displays network connections and listening ports.
    - Key options:
      - `netstat -a` all connections/ports
      - `netstat -at` TCP only
      - `netstat -au` UDP only
      - `netstat -l` listening ports
      - `netstat -s` protocol stats
      - `netstat -tp` shows PID/program for connections (requires root for all info)
      - `netstat -i` interface stats
      - `netstat -ano` common combined usage

15. **find**
    - Searches filesystem for files/directories.
    - Examples:
      - `find / -name flag1.txt` find file by name
      - `find / -type d -name config` find directory by name
      - `find / -perm 0777` find files with 777 perms
      - `find / -perm a=x` find executable files
      - `find /home -user frank` files owned by user frank
      - `find / -mtime 10` modified in last 10 days
      - `find / -cmin -60` changed in last 60 mins
      - `find / -size 50M` files of 50 MB size
      - Use `2>/dev/null` to suppress errors

    - Search for writable/executable folders:
      - `find / -writable -type d 2>/dev/null`
      - `find / -perm -o w -type d 2>/dev/null`
      - `find / -perm -o x -type d 2>/dev/null`

    - Search for dev tools/languages:
      - `find / -name perl*`
      - `find / -name python*`
      - `find / -name gcc*`

    - Find SUID files (privilege escalation vectors):
      - `find / -perm -u=s -type f 2>/dev/null`

Summary:
Post-access enumeration involves commands to identify system details, processes, users, environment, network, and potential privilege escalation vectors. Each command uncovers specific data critical for planning lateral movement, privilege escalation, or data exfiltration.
