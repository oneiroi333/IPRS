# IPRS
IP reputation system

This software implements web crawlers that gather IP address information from publicly accessible OSINT feeds.
For every collected IP address a Whois lookup is made. The whole information packet is then stored in a MongoDB Database.
To launch the data collection process execute the file 'crawler.py'.

If you want to lookup an IP address from the database you can do so by using 'lookup.py' with the IP address as only argument.
