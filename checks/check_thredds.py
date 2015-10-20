#!/usr/bin/env python
'''
checks/check_thredds.py
'''

from netCDF4 import Dataset
from datetime import datetime, timedelta
import requests
import sys

def check_das(url):
    das_url = url + '.das'
    response = requests.get(das_url)
    if response.status_code != 200:
        print "Failed to acquire DAS for %s" % url
        return False
    return True

def check(url):
    try:
        with Dataset(url) as nc:
            return True
    except:
        print "Failed to load dataset"
    return False

def check_recent(url):
    with Dataset(url) as nc:
        if 'time' not in nc.variables:
            print 'Could not identify time variable'
            return False

        timestamp = nc.variables['time'][-1]

    threshold = datetime.utcnow() - timedelta(hours=6)
    datetimestamp = datetime.utcfromtimestamp(timestamp)
    if datetimestamp < threshold:
        print "Data is not recent"
        return False
    return True

def main(args):
    '''
    Checks for the existence of a dataset
    '''
    if not check_das(args.url):
        return 1
    if not check(args.url):
        return 1
    if args.time:
        if not check_recent(args.url):
            return 1
    print "Dataset is alive"
    return 0

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument('-t', '--time', action='store_true', help='Check the data is recent')
    parser.add_argument('url', help='Source dataset to check and identify')
    args = parser.parse_args()
    sys.exit(main(args))
