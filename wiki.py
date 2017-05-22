#!/usr/bin/env python3

import argparse
import requests
import re

API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'


class PageNotFoundError(Exception):
    pass


def get_wiki_summary(title):
    """
    Return the wikipedia extract of the page for title
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
        raise PageNotFoundError

    summary = r[pageid]['extract']
    return summary


def get_disambiguation_list(title):
    """
    Return a list of all the titles on the disambiguation page for
    title
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
        raise PageNotFoundError

    r = r[pageid]
    titles = [link['title'] for link in r['links'] if link['ns'] == 0]
    return titles


def get_disambiguation_title(title, index):
    """
    Return the title in the disambiguation title list at index
    """
    if index <= 0:
        raise IndexError
    titles = get_disambiguation_list(title)
    if index > len(titles):
        raise IndexError

    return titles[index-1]


def get_page_url(title):
    """Returns the url for the given title
    """
    params = {
        'action': 'query',
        'prop': 'info',
        'format': 'json',
        'inprop': 'url',
        'titles': title
    }
    r = requests.get(API_ENDPOINT, params=params)
    r = r.json()['query']['pages']
    pageid = next(iter(r.keys()))

    if pageid == '-1':
        raise PageNotFoundError

    url = r[pageid]['fullurl']
    return url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='title of page to search for')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list-disambiguations', action='store_true',
                       help='list all disambiguations for the given TITLE')
    group.add_argument('-d', '--disambiguation', type=int,
                       help='choose the Nth disambiguation for TITLE')
    parser.add_argument('-u', '--url', action='store_true',
                        help='output the url of the page')
    args = parser.parse_args()
    title = args.title.strip()

    # Prevents string.title() from changing what's inside parentheses
    # Searches for words in parens at the end of the line
    m = re.search('(\([A-Za-z]*\)$)', title)
    if m is not None:
        title = '{} {}'.format(
            title.replace(m.group(), '').strip().title(),
            m.group()
        )

    if args.list_disambiguations:
        try:
            titles = get_disambiguation_list(title)
            for i, t in enumerate(titles, start=1):
                print('{} - {}'.format(i, t))
        except PageNotFoundError:
            parser.error('no disambiguations found for: \'{}\''.format(title))
    elif args.disambiguation is not None:
        try:
            index = args.disambiguation
            title = get_disambiguation_title(title, index)
            summary = get_wiki_summary(title)
            print(summary)
        except IndexError:
            parser.error('disambiguation index out of range')
    else:
        try:
            summary = get_wiki_summary(title)
            print(summary)
        except PageNotFoundError:
            parser.error('no page found for: \'{}\''.format(title))

    if args.url:
        try:
            url = get_page_url(title)
            print(url)
        except PageNotFoundError:
            parser.error('no url found for: \'{}\''.format(title))

if __name__ == '__main__':
    main()
