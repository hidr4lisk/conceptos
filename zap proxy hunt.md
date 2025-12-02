 Let’s install the bugcrowd HUNT extensions for OWASP ZAP. This will passively scan for known vulnerabilities in web applications.


First navigate in your terminal somewhere you’d like to store the scripts

` git clone https://github.com/bugcrowd/HUNT `


Then in ZAP click the “Manage Add-Ons” icon


From the Marketplace install “Python Scripting” and “Community Scripts”


In ZAP Options, under Passive Scanner, make sure “Only scan messages in scope” is enabled. Then hit OK.



In ZAP open the Scripts tab.

And under Passive Rules, find and enable the HUNT.py script


Now when you browse sites and HUNT will passively scan for SQLi, LFI, RFI, SSRF, and others. Exciting!