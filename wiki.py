#!/usr/bin/env python3

import argparse
import requests
import re

# --- Exceptions ---
class PageNotFoundError(Exception):
    """Custom exception when a Wikipedia page is not found."""
    pass

class DisambiguationNotFoundError(PageNotFoundError):
    """Custom exception when a disambiguation page has no valid entries."""
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
        raise PageNotFoundError('Page not found')
    
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
    page = fetch_wiki_data(params)
    links = page.get('links', [])

    if not links:
        raise DisambiguationNotFoundError(f'No disambiguations found for: "{title}"')

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

def handle_list_disambiguations(title, parser):
    titles = get_disambiguation_list(title)
    for i, title in enumerate(titles, 1):
        print(f'{i} - {title}')

def handle_disambiguation_summary(title, index, parser):
    try:
        selected_title = get_disambiguation_title(title, index)
        summary = get_summary(selected_title)
        print(summary)
    except IndexError:
        parser.error('disambiguation index out of range')

def handle_summary(title, parser):
    try:
        summary = get_summary(title)
        print(summary)
    except PageNotFoundError:
        parser.error(f'No page found for: "{title}"')

def handle_url(title, parser):
    try:
        url = get_page_url(title)
        print(url)
    except PageNotFoundError:
        parser.error(f'No URL found for: "{title}"')

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    title = args.title.strip()

    if args.list_disambiguations:
        handle_list_disambiguations(title, parser)
    elif args.disambiguation is not None:
        handle_disambiguation_summary(title, args.disambiguation, parser)
    else:
        handle_summary(title, parser)

    if args.url:
        handle_url(title, parser)


if __name__ == '__main__':
    main()
