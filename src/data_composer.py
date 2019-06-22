import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from .crawler.crawler_manager import CrawlerManager
from .whois import Whois
from .utils import print_log, TIME_FRMT_LOG


class DataComposer():

    def __init__(self,
            verbose = False,
            host = 'localhost',
            port = 27017,
            user = None,
            pw = None,
            db = 'iprs'
        ):
        self.verbose = verbose
        self._time_frmt_log = TIME_FRMT_LOG
        self.mongodb = {
            'host': host,
            'port': port,
            'user': user,
            'pw': pw,
            'db': db
        }
        self._conn = None
        self._crawler_manager = CrawlerManager(
            verbose = self.verbose,
            crawler_result_callback = self._process_crawler_result
        )

    def start(self):
        if self.verbose:
            print_log(self._time_frmt_log, '[{}] Start'.format(self.__class__.__name__))
            
        client = MongoClient(
            host = self.mongodb['host'],
            port = self.mongodb['port'],
            username = self.mongodb['user'],
            password = self.mongodb['pw']
        )
        # Check the connection to the mongo db
        try:
            client.admin.command('ismaster')
        except ConnectionFailure:
            if self.verbose:
                print_log(self._time_frmt_log, '[{}] Connection to MongoDB ({}:{}) failed! Exiting...'.format(self.__class__.__name__, self.mongodb['host'], self.mongodb['port']))
            client.close()
            raise RuntimeError

        self._conn = client[self.mongodb['db']]
        self._crawler_manager.start()
        client.close()
        if self.verbose:
            print_log(self._time_frmt_log, '[{}] Finish'.format(self.__class__.__name__))

    def _process_crawler_result(self, crawler_result):
        # Process the iplists
        iplist_name_to_db_id_map = {}
        # Get the names of the crawled iplists
        iplist_rec_names = [x for x in crawler_result.iplist_records]
        # Search the db for the iplists
        coll = self._conn['ip_addr_list']
        db_records = list(coll.find({'name': {'$in': iplist_rec_names}}))

        # Update/insert the iplists
        for name in iplist_rec_names:
            iplist_rec = crawler_result.iplist_records[name]
            db_rec = next(filter(lambda rec: rec['name'] == name, db_records), None)
            if db_rec: # update
                rec_id = db_rec['_id']
                coll.update_one(
                    {'_id': rec_id},
                    {'$set': {'date_last_fetch': str(datetime.now())}}
                )
            else: # insert
                json_rec = json.loads(json.dumps(iplist_rec.__dict__, default=str))
                rec_id = coll.insert_one(json_rec).inserted_id
            iplist_name_to_db_id_map.update({name: rec_id})

        # Process the ips
        ip_rec_ip_addresses = [x for x in crawler_result.ip_records]
        # Search the db for the ips
        coll = self._conn['ip_addr']
        db_records = list(coll.find({'ip_address': {'$in': ip_rec_ip_addresses}}))
        # Update/insert the ip
        for ip_addr in ip_rec_ip_addresses:
            # TODO whois lookup should be an external service, else this takes ages
            # Whois lookup
            #whois = Whois(ip_addr).lookup()
            whois = None

            ip_rec = crawler_result.ip_records[ip_addr]
            db_rec = next(filter(lambda rec: rec['ip_address'] == ip_addr, db_records), None)

            if db_rec: # update
                # Update iplist references
                iplists = crawler_result.ip_to_iplist_map[ip_addr]
                iplist_ids = [iplist_name_to_db_id_map[iplist_name] for iplist_name in iplists]
                iplist_refs = db_rec['iplist_refs']
                iplist_refs_new = list(set(iplist_ids + iplist_refs))

                # Update tags
                tags = db_rec['tags']
                for tag in ip_rec.tags:
                    tags.update({tag: ip_rec.tags[tag] or tags[tag]})

                coll.update_one(
                    {'_id': db_rec['_id']},
                    {'$set': {
                        'date_last_seen': str(datetime.now()),
                        'tags': tags,
                        'whois': whois,
                        'iplist_refs': iplist_refs_new
                    }}
                )
            else: # insert
                iplists = crawler_result.ip_to_iplist_map[ip_addr]
                iplist_ids = [iplist_name_to_db_id_map[iplist_name] for iplist_name in iplists]
                ip_rec.whois = whois
                json_rec = json.loads(json.dumps(ip_rec.__dict__, default=str))
                json_rec['iplist_refs'] = iplist_ids
                coll.insert_one(json_rec)
