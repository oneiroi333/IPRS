from ipwhois import IPWhois
from pprint import pprint

def main():
    whois_h = IPWhois('193.99.144.85') # heise.de
    #whois_h = IPWhois('151.101.194.49') # zeit.de
    result = whois_h.lookup_rdap()
    pprint(result)

if __name__ == "__main__":
    main()
