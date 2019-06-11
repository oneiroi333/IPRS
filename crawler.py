#!/usr/bin/env python3

import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    cmd_group = parser.add_mutually_exclusive_group()
    cmd_group.add_argument('add', help='Add crawler to the pool. Name must match the filename in src/crawler/CrawlerXXX')
    cmd_group.add_argument('rm', help='Remove crawler from the pool')
    cmd_group.add_argument('start', help='Start the crawling process')
    parser.add_argument('-v', '--verbose', help='Print information to stdout')
    args = parser.parse_args()

    verbose = False
    dir_path = os.path.dirname(os.path.realpath(__file__))
    active_crawler_path = dir_path + '/active_crawler'
    crawler_src_path = dir_path + '/src/crawler/'

    if (args.verbose):
        verbose = True

    if (args.add):
        exists = os.path.isfile(crawler_src_path + args.add + '.py')
        if exists:
            os.symlink(crawler_src_path + args.add + '.py', active_crawler_path + args.add)
        else:
            print('No crawler with name \'{}\' in \'{}\''.format(args.add, crawler_src_path))
    elif (args.rm):
        exists = os.path.isfile(active_crawler_path + args.add)
        if exists:

    elif (args.start):



if __name__ == "__main__":
    main()
