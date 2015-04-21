#!/usr/bin/env python
'''
mirrors.py: 
- download list of cygwin rsync mirrors
- time download setup.bz2 from each mirror
- print results

Requires: 
- BeautifulSoup
- requests
'''
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import time


def get_mirrors():
    timeout_time = 30
    url = 'https://cygwin.com/mirrors.html'
    try:
        r = requests.get(url, timeout=timeout_time)
    except Exception as e:
        print('get_mirrors: exception in get for %s: %s' % (url, e))
        return ''
    return r.text


def get_rsyncs(mirrors):
    rsyncs = []
    soup = BeautifulSoup(mirrors)
    for link in soup.find_all('a'):
        u = link.get('href')
        if u and u.find('rsync') == 0:
            rsyncs.append(u)
    return rsyncs


def as_http(url):
    return url.replace('rsync://', 'http://')


def download_setup(rsync):
    f = 'x86_64/setup.bz2'
    url = as_http(rsync) + f
    timeout_time = 30
    try:
        r = requests.get(url, timeout=timeout_time)
    except Exception as e:
        print('download_setup: exception in get for %s: %s' % (url, e))
        return False
    return True


def time_downloads(rsyncs):
    times = []
    for r in rsyncs:
        start_time = time.time()
        done = download_setup(r)
        end_time = time.time()
        if done:
            times.append({
                'rsync': r,
                'time': end_time - start_time
            })
    return times


def sort_rsyncs(rsyncs):
    def cmp_time(a, b):
        return cmp(a['time'], b['time'])
    return sorted(rsyncs, cmp_time)


def print_results(rsyncs):
    for r in rsyncs:
        print('%(rsync)s %(time).3f' % r)


def main():
    print_results(sort_rsyncs(time_downloads(get_rsyncs(get_mirrors()))))


if __name__ == '__main__':
    main()

