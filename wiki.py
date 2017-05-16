#!/usr/bin/env python3

import argparse
import requests


def get_wiki_summary(title):
    API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'
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
        r = r[pageid]
        page_title = r['title']
        summary = r['extract']
        print(page_title)
        print(summary)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title of page to search for')
    args = parser.parse_args()

    get_wiki_summary(args.title)


if __name__ == '__main__':
    main()
