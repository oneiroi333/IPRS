import ipaddress
from datetime import datetime


TIME_FRMT_LOG = '%H:%M:%S'

def print_log(time_frmt, msg):
    print('[{}] {}'.format(datetime.now().strftime(time_frmt), msg))


def extract_ip_addr_all(data):
    ip_addr_all = {
        'ipv4': set(),
        'ipv6': set()
    }
    lines = data.splitlines()
    for line in lines:
        try:
            ip_addr = ipaddress.ip_address(line.strip())
        except ValueError:
            # Not an IP address
            continue

        if isinstance(ip_addr, ipaddress.IPv4Address):
            ip_addr_all['ipv4'].add(str(ip_addr))
        elif isinstance(ip_addr, ipaddress.IPv6Address):
            ip_addr_all['ipv6'].add(str(ip_addr))

    return ip_addr_all
