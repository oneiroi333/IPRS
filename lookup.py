#!/usr/bin/env python3

import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print('{} <ip address>'.format(sys.argv[0]))
        sys.exit(1)

    ip_addr = sys.argv[1]
    client = MongoClient(
        host = 'localhost',
        port = 27017,
        username = None,
        password = None
    )
    # Check the connection to the mongo db
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        client.close()
        sys.exit(1)

    conn = client['iprs']
    coll = conn.ip_addr
    result = list(coll.aggregate([
        {'$unwind': '$iplist_refs'},
        {'$lookup': {
            'from': 'ip_addr_list',
            'localField': 'iplist_refs',
            'foreignField': '_id',
            'as': 'iplist_refs'
        }},
        {'$match': {
            'ip_address': {'$eq': ip_addr}
        }}
    ]))
    if result:
        print_result(result[0])
    else:
        print('No record found')
    client.close()

def print_result(result):
    print('Record found')

    print('\n[ Info address ]')
    print('IP address: {}'.format(result['ip_address']))
    print('IP version: {}'.format(result['ip_version']))
    print('Tags:')
    for tag in result['tags']:
        if result['tags'][tag]:
            print('  {}'.format(tag))
    print('Date first seen: {}'.format(datetime.strptime(result['date_created'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')))
    print('Date last seen: {}'.format(datetime.strptime(result['date_last_seen'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')))

    print('\n[ Info lists ]')
    for iplist in result['iplist_refs']:
        print('Name: {}'.format(iplist['name']))
        print('Source URL: {}'.format(iplist['src_url']))
        if iplist['managed_by']['name'] or iplist['managed_by']['url']:
            print('Managed by:')
            if iplist['managed_by']['name']:
                print('  Name: {}'.format(iplist['managed_by']['name']))
            if iplist['managed_by']['url']:
                print('  URL: {}'.format(iplist['managed_by']['url']))
        print('Date first fetch: {}'.format(datetime.strptime(iplist['date_created'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')))
        print('Date last fetch: {}'.format(datetime.strptime(iplist['date_last_fetch'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')))

    whois = result['whois']
    if whois:
        print('\n[ Info whois ]')
        as_ = whois.get('as') 
        if as_:
            print('Autonomous System:')
            if as_.get('number'):
                print('  Number: {}'.format(as_.get('number')))
            if as_.get('description'):
                print('  Description: {}'.format(as_.get('description')))
            if as_.get('country_code'):
                print('  Country code: {}'.format(as_.get('country_code')))
            if as_.get('registry'):
                print('  Registry: {}'.format(as_.get('registry')))
            if as_.get('allocation_date'):
                print('  Allocation date: {}'.format(as_.get('allocation_date')))
        network = whois.get('network') 
        if network:
            print('Network:')
            if network.get('name'):
                print('  Name: {}'.format(network.get('name')))
            if network.get('country'):
                print('  Country: {}'.format(network.get('country')))
            if network.get('cidr'):
                print('  CIDR: {}'.format(network.get('cidr')))
            if network.get('start_address'):
                print('  Start address: {}'.format(network.get('start_address')))
            if network.get('end_address'):
                print('  End address: {}'.format(network.get('end_address')))
            if network.get('ip_version'):
                print('  IP version: {}'.format(network.get('ip_version')))
            if network.get('status'):
                print('  Status: {}'.format(network.get('status')))
            if network.get('registration_date'):
                print('  Registartion date: {}'.format(datetime.strptime(network.get('registartion_date'), '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')))
            if network.get('last_changed_date'):
                print('  Last changed date: {}'.format(datetime.strptime(network.get('last_changed_date'), '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')))
        entities = whois.get('entities') 
        if entities:
            print('Entities:')
            for entity in entities:
                contact = entity.get('entity')
                if contact:
                    print('  Contact:')
                    if contact.get('name'):
                        print('    Name: {}'.format(contact.get('name')))
                    if contact.get('kind'):
                        print('    Kind: {}'.format(contact.get('kind')))
                    if contact.get('address'):
                        print('    Address:')
                        for idx, addr in enumerate(contact.get('address'), start=1):
                            print('      {}: {}'.format(idx, addr))
                    if contact.get('phone'):
                        print('    Phone: {}'.format(contact.get('phone')))
                    if contact.get('email'):
                        print('    Email:')
                        for idx, email in enumerate(contact.get('email'), start=1):
                            print('      {}: {}'.format(idx, email))
                if entity.get('roles'):
                    print('  Roles:')
                    for idx, role in enumerate(entity.get('roles'), start=1):
                        print('    {}: {}'.format(idx, role))
                if entity.get('status'):
                    print('  Status: {}'.format(entity.get('status')))


if __name__ == '__main__':
    main()
