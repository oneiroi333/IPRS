#!/usr/bin/env python3

import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--add', help='Add crawler to the pool. Name must match the filename in src/crawler/XXX without fileextension')
    group.add_argument('--rm', help='Remove crawler from the pool')
    group.add_argument('--start', help='Start the crawling process', action='store_true')
    parser.add_argument('-v', '--verbose', help='Print more information', action='store_true')
    args = parser.parse_args()

    verbose = False
    if (args.verbose):
        verbose = True

    dir_path = os.path.dirname(os.path.realpath(__file__))
    active_crawler_path = dir_path + '/active_crawler'
    crawler_src_path = dir_path + '/src/crawler/'

    if (args.add):
        exists = os.path.isfile(os.path.join(crawler_src_path, args.add + '.py'))
        if exists:
            os.symlink(os.path.join(crawler_src_path, args.add + '.py'), os.path.join(active_crawler_path, args.add))
            if verbose:
                print("Crawler added '{}'".format(args.add))
        else:
            if verbose:
                print("No crawler named '{}' in '{}'".format(args.add, crawler_src_path))
    elif (args.rm):
        exists = os.path.islink(os.path.join(active_crawler_path, args.rm))
        if exists:
            os.remove(os.path.join(active_crawler_path, args.rm))
            if verbose:
                print("Crawler removed '{}'".format(args.rm))
        else:
            if verbose:
                print("No active crawler named '{}'".format(args.rm))
    elif (args.start):
        import importlib.util

        spec = importlib.util.spec_from_file_location('CrawlerManager', crawler_src_path + 'CrawlerManager.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if verbose:
            print("Crawling process started")

        manager = CrawlerManager()
        '''
        manager = CrawlerManager(verbose=verbose)
        manager.registerCrawler()
        '''
        manager.start()


if __name__ == "__main__":
    main()
