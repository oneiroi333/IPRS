import sys
from pprint import pprint


# Usage
if len(sys.argv) < 2:
    print('{} <ip>'.format(sys.argv[0]))
    sys.exit(1)

ip_addr = sys.argv[1]
client = MongoClient(
    host = 'localhost',
    port = 27017,
    username = 'bla',
    password = 'blubb'
)
# Check the connection to the mongo db
try:
    client.admin.command('ismaster')
except ConnectionFailure:
    client.close()
    sys.exit(1)

conn = client['iprs'] # db name: iprs
coll = conn.ip_addr # collection name: ip_addr
result = coll.find({'ip_address': ip_addr})
if result:
    pprint(result)
else:
    print('No record found')
client.close()
