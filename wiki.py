#!/usr/bin/env python3

import argparse
import requests
import re

# --- Exceptions ---
class PageNotFoundError(Exception):
    pass

# --- Wikipedia API Utilities ---
def fetch_wiki_data(params):
    """Make a request to the Wikipedia API and return the result."""
    WIKI_API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'
    default_params = {'action': 'query', 'format': 'json'}
    params.update(default_params)
    response = requests.get(WIKI_API_ENDPOINT, params=params).json()

    pages = response['query']['pages']
    pageid = next(iter(pages.keys()))
    page = pages[pageid]

    if pageid == '-1':
        raise PageNotFoundError
    
    return page

# --- Wikipedia Functionality ---

def get_summary(title):
    """Return the wikipedia extract (summary) for the given title."""
    params = {
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': '',
        'titles': title
    }
    summary = fetch_wiki_data(params)['extract']

    return summary

def get_page_url(title):
    """Returns the full Wikipedia url for a given title."""
    params = {
        'prop': 'info',
        'inprop': 'url',
        'titles': title
    }
    url = fetch_wiki_data(params)['fullurl']

    return url

def get_disambiguation_list(title):
    """Return a list of possible disambiguation titles."""
    params = {
        'titles': '{} (disambiguation)'.format(title),
        'prop': 'links'
    }
    links = fetch_wiki_data(params)['links']
    titles = [link['title'] for link in links if link['ns'] == 0]

    return titles


def get_disambiguation_title(title, index):
    """Return the Nth title from the disambiguation list."""
    titles = get_disambiguation_list(title)
    if index < 1 or index > len(titles):
        raise IndexError('Invalid disambiguation index.')
    title = titles[index - 1]

    return title

# --- Argument Parsing and CLI Logic ---

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Get Wikipedia Summaries.')
    parser.add_argument('title', help='Title of the page to search for')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list-disambiguations', action='store_true',
                       help='List all disambiguation options')
    group.add_argument('-d', '--disambiguation', type=int,
                       help='Use the Nth disambiguation')
    
    parser.add_argument('-u', '--url', action='store_true',
                        help='Output the page url')

    return parser

def process_list_disambiguations(title, parser):
    try:
        title_list = get_disambiguation_list(title)
        for i, title in enumerate(title_list, start=1):
            print('{} - {}'.format(i, title))
    except PageNotFoundError:
        parser.error('no disambiguations found for: \'{}\''.format(title))

def process_disambiguation_selection(args, parser):
    try:
        disambiguation_selection = args.disambiguation
        title = get_disambiguation_title(title, disambiguation_selection)
        summary = get_summary(title)
        print(summary)
    except IndexError:
        parser.error('disambiguation index out of range')

def process_wiki_summary(title, parser):
    try:
        summary = get_summary(title)
        print(summary)
    except PageNotFoundError:
        parser.error('no page found for: \'{}\''.format(title))   
    


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    title = args.title.strip()

    if args.list_disambiguations:
        process_list_disambiguations(title, parser)
    elif args.disambiguation is not None:
        process_disambiguation_selection(args, parser)
    else:
        process_wiki_summary(title, parser)

    if args.url:
        try:
            url = get_page_url(title)
            print(url)
        except PageNotFoundError:
            parser.error('no url found for: \'{}\''.format(title))

if __name__ == '__main__':
    main()
