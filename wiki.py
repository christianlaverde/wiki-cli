#!/usr/bin/env python3

import argparse
import requests
import re

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
        return None
    else:
        summary = r[pageid]['extract']
        return summary


def get_disambiguation_list(title):
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
        return None
    else:
        r = r[pageid]
        titles = [link['title'] for link in r['links'] if link['ns'] == 0]
        return titles


def get_disambiguation_title(title, index):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title of page to search for')
    parser.add_argument('-l', '--list-disambiguations', action='store_true',
                        help='List all disambiguations for the given title')
    args = parser.parse_args()
    title = args.title.strip()

    m = re.search('\(.*\)', title)
    if m is not None:
        title = '{} {}'.format(
            title.replace(m.group(), '').strip().title(),
            m.group()
        )

    if args.list_disambiguations:
        titles = get_disambiguation_list(title)
        if titles is not None:
            for i, title in enumerate(titles, start=1):
                print('{} - {}'.format(i, title))
        else:
            print('No disambiguations found for: \'{}\''.format(title))
    else:
        summary = get_wiki_summary(title)
        if summary is not None:
            print(summary)
        else:
            print('No page found for: \'{}\''.format(title))
if __name__ == '__main__':
    main()
