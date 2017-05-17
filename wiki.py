#!/usr/bin/env python3

import argparse
import requests

API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'


def get_wiki_summary(title):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': '',
        'titles': title
    }
    r = requests.get(API_ENDPOINT, params=params)
    r = r.json()['query']['pages']
    pageid = next(iter(r.keys()))

    if pageid == '-1':
        print('No page found for: \'{}\''.format(title))
    else:
        summary = r[pageid]['extract']
        print(summary)


def get_disambiguation_titles(title):
    params = {
        'action': 'query',
        'format': 'json',
        'titles': '{} (disambiguation)'.format(title),
        'prop': 'links'
    }
    r = requests.get(API_ENDPOINT, params=params)
    r = r.json()['query']['pages']
    pageid = next(iter(r.keys()))

    if pageid == '-1':
        print('No disambiguations found for: \'{}\''.format(title))
    else:
        r = r[pageid]
        for link_num, link in enumerate(r['links'], start=1):
            if link['ns'] == 0:
                print('{} - {}'.format(link_num, link['title']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title of page to search for')
    parser.add_argument('-l', '--list-disambiguations', action='store_true',
                        help='List all disambiguations for the given title')
    args = parser.parse_args()
    title = args.title.strip()

    if args.list_disambiguations:
        get_disambiguation_titles(title)
    else:
        get_wiki_summary(title)

if __name__ == '__main__':
    main()
