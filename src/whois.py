from ipwhois import IPWhois


class Whois():

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self._whois = IPWhois(ip_addr)

    def lookup(self):
        res = self._whois.lookup_rdap(
            asn_methods = ['whois'],
            retry_count = 5
        )

        result = None
        if res:
            result = {}
            result['as'] = {
                'number': res.get('asn'),
                'country_code': res.get('asn_country_code'),
                'allocation_date': res.get('asn_date'),
                'description': res.get('asn_description'),
                'registry': res.get('asn_registry'),
            }
            network = res.get('network')
            if network:
                registration_date = None
                last_changed_date = None
                events = network.get('events')
                if events:
                    for e in events:
                        if e['action'] == 'registration':
                            registration_date = e['timestamp']
                        elif e['action'] == 'last changed':
                            last_changed_date = e['timestamp']
                result['network'] = {
                    'name': network.get('name'),
                    'cidr': network.get('cidr'),
                    'start_address': network.get('start_address'),
                    'end_address': network.get('end_address'),
                    'ip_version': network.get('ip_version'),
                    'country': network.get('country'),
                    'status': network.get('status'),
                    'registration_date': registration_date,
                    'last_changed_date': last_changed_date
                }

            result['entities'] = []
            objects = res.get('objects')
            if objects:
                for entity_name in res.get('entities'):
                    if objects.get(entity_name):
                        entity = objects.get(entity_name)

                        contact = entity.get('contact') 
                        if contact:
                            addresses = None
                            address = contact.get('address')
                            if address:
                                addresses = []
                                for addr in address:
                                    if addr.get('value'):
                                        addresses.append(addr.get('value'))

                            emails = None
                            email = contact.get('email')
                            if email:
                                emails = []
                                for em in email:
                                    if em.get('value'):
                                        emails.append(em.get('value'))

                            contact = {
                                'name': contact.get('name'),
                                'kind': contact.get('kind'),
                                'address': addresses,
                                'email': emails,
                                'phone': contact.get('phone'),
                            }
                        result['entities'].append({
                            'contact': contact,
                            'roles': entity.get('roles'),
                            'status': entity.get('status')
                        })

        return result
