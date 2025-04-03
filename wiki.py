#!/usr/bin/env python3

import argparse
import requests
import re

class PageNotFoundError(Exception):
    pass


def get_wiki_summary(title):
    """
    Return the wikipedia extract of the page for title
    """
    params = {
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': '',
        'titles': title
    }
    result  = get_result(params)

    summary = result['extract']
    return summary


def get_disambiguation_title_list(title):
    """
    Return a list of all the titles on the disambiguation page for
    title
    """
    params = {
        'titles': '{} (disambiguation)'.format(title),
        'prop': 'links'
    }
    result  = get_result(params)

    titles = [link['title'] for link in result['links'] if link['ns'] == 0]
    return titles


def get_disambiguation_title(title, index):
    """
    Return the title in the disambiguation title list at index
    """
    if index <= 0:
        raise IndexError
    titles = get_disambiguation_title_list(title)
    if index > len(titles):
        raise IndexError

    return titles[index-1]


def get_page_url(title):
    """Returns the url for the given title
    """
    params = {
        'prop': 'info',
        'inprop': 'url',
        'titles': title
    }
    result  = get_result(params)

    url = result['fullurl']
    return url

def get_result(params):
    API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'
    default_params = {'action': 'query', 'format': 'json'}
    params.update(default_params)
    result = requests.get(API_ENDPOINT, params=params).json()
    result = result['query']['pages']
    pageid = next(iter(result.keys()))
    result = result[pageid]

    if pageid == '-1':
        raise PageNotFoundError
    
    return result

def createParser():
    parser = argparse.ArgumentParser(
        description='Get summaries from Wikipedia')
    parser.add_argument('title', help='title of page to search for')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list-disambiguations', action='store_true',
                       help='list all disambiguations for the given TITLE')
    group.add_argument('-d', '--disambiguation', type=int,
                       help='choose the Nth disambiguation for TITLE')
    parser.add_argument('-u', '--url', action='store_true',
                        help='output the url of the page')

    return parser

def process_list_disambiguations(title, parser):
    try:
        title_list = get_disambiguation_title_list(title)
        for i, title in enumerate(title_list, start=1):
            print('{} - {}'.format(i, title))
    except PageNotFoundError:
        parser.error('no disambiguations found for: \'{}\''.format(title))

def process_disambiguation_selection(args, parser):
    try:
        disambiguation_selection = args.disambiguation
        title = get_disambiguation_title(title, disambiguation_selection)
        summary = get_wiki_summary(title)
        print(summary)
    except IndexError:
        parser.error('disambiguation index out of range')

def process_wiki_summary(title, parser):
    try:
        summary = get_wiki_summary(title)
        print(summary)
    except PageNotFoundError:
        parser.error('no page found for: \'{}\''.format(title))   
    


def main():
    parser = createParser()
    args = parser.parse_args()
    title = args.title.strip()

    # Prevents string.title() from changing what's inside parentheses
    # Searches for words in parens at the end of the line
    m = re.search(r'(\([A-Za-z]*\)$)', title)
    if m is not None:
        title = title.replace(m.group(), '').strip().title()
        title = '{} {}'.format(title, m.group())
    else:
        title = title.title()

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
