# wiki-cli
A command line interface to retrieve summaries from Wikipedia

# Usage
```
usage: wiki.py [-h] [-l] title

positional arguments:
  title                 Title of page to search for

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-disambiguations
                        List all disambiguations for the given title

```

# Examples
```
$ ./wiki.py "Wikipedia"

Wikipedia (/ˌwɪkᵻˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a free
online encyclopedia with the aim to allow anyone to edit
articles. Wikipedia is the largest and most popular general reference
work on the Internet and is ranked among the ten most popular
websites. Wikipedia is owned by the nonprofit Wikimedia Foundation.
Wikipedia was launched on January 15, 2001, by Jimmy Wales and Larry
Sanger. Sanger coined its name, a portmanteau of wiki and
encyclopedia. There was only the English language version initially,
but it quickly developed similar versions in other languages, which
differ in content and in editing practices. With 5,406,746 articles,
the English Wikipedia is the largest of the more than 290 Wikipedia
encyclopedias. Overall, Wikipedia consists of more than 40 million
articles in more than 250 different languages and, as of February
2014, it had 18 billion page views and nearly 500 million unique
visitors each month.  As of March 2017, Wikipedia has about forty
thousand high-quality articles known as Featured Articles and Good
Articles that cover vital topics. In 2005, Nature published a peer
review comparing 42 science articles from Encyclopædia Britannica and
Wikipedia, and found that Wikipedia's level of accuracy approached
Encyclopædia Britannica's. Criticism of Wikipedia includes claims that
it exhibits systemic bias, presents a mixture of "truths, half truths,
and some falsehoods", and that, in controversial topics, it is subject
to manipulation and spin.
```

```
$ ./wiki.py "Philosophy" -l

2 - Philosophy
3 - Philosophy: The Best of Bill Hicks
4 - Philosophy (Ben Folds Five song)
5 - Philosophy (album)
6 - Philosophy (journal)
7 - Philosophy of life
8 - Salvator Rosa
9 - Tom Snare1 - Philosophical theory
```