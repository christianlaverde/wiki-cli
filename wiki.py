#!/usr/bin/env python3

import argparse
import requests
import re

API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'


def get_wiki_summary(title):
    """
    Return the wikipedia extract of the page for title, or None if no
    page is found
    """
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
    """
    Return a list of all the titles on the disambiguation page for
    title or None if no page is found
    """
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
    """
    Return the title in the disambiguation title list at index or None
    if index is too large
    """
    titles = get_disambiguation_list(title)
    if index > len(titles):
        return None
    else:
        return titles[index-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='Title of page to search for')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list-disambiguations', action='store_true',
                       help='List all disambiguations for the given TITLE')
    group.add_argument('-d', '--disambiguation', type=int,
                       help='Choose the Nth disambiguation for TITLE')
    args = parser.parse_args()
    title = args.title.strip()

    # Prevents .title() from changing what's inside parentheses
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
            parser.error('No disambiguations found for: \'{}\''.format(title))
    elif args.disambiguation is not None:
        index = args.disambiguation
        if index <= 0:
            parser.error('Disambiguation index must be a positive integer')
        title = get_disambiguation_title(title, index)
        if title is not None:
            summary = get_wiki_summary(title)
            print(summary)
        else:
            parser.error('Disambiguation index too large')
    else:
        summary = get_wiki_summary(title)
        if summary is not None:
            print(summary)
        else:
            parser.error('No page found for: \'{}\''.format(title))

if __name__ == '__main__':
    main()
