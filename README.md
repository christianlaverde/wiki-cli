# wiki-cli
A command line interface to retrieve summaries from Wikipedia

# Usage
```
usage: wiki.py [-h] [-l | -d DISAMBIGUATION] [-u] title

Get Wikipedia Summaries.

positional arguments:
  title                 Title of the page to search for

options:
  -h, --help            show this help message and exit
  -l, --list-disambiguations
                        List all disambiguation options
  -d, --disambiguation DISAMBIGUATION
                        Use the Nth disambiguation
  -u, --url             Output the page url
```

# Examples
```
$ ./wiki.py git
Git (/ɡɪt/) is a version control system (VCS) for
tracking changes in computer files and coordinating work on those
files among multiple people. It is primarily used for softwa re
development, but it can be used to keep track of changes in any
files. As a distribut ed revision control system it is aimed at speed,
data integrity, and support for distrib uted, non-linear workflows.
Git was created by Linus Torvalds in 2005 for development of the Linux
kernel, with othe r kernel developers contributing to its initial
development. Its current maintainer sinc e 2005 is Junio Hamano.  As
with most other distributed version control systems, and unlike most
client–server sy stems, every Git directory on every computer is a
full-fledged repository with complete history and full version
tracking abilities, independent of network access or a central server.
Like the Linux kernel, Git is free software distributed under the
terms of the GNU Gener al Public License version 2.

```

```
$ ./wiki.py "Philosophy" -l
1 - Philosophical theory
2 - Philosophy
3 - Philosophy: The Best of Bill Hicks
4 - Philosophy (Ben Folds Five song)
5 - Philosophy (Salvator Rosa)
6 - Philosophy (album)
7 - Philosophy (brand)
8 - Philosophy (journal)
9 - Philosophy of life
10 - Tom Snare
```

```
$ ./wiki.py "Philosophy" -d 10
Xavier Decanter (French pronunciation: [ɡzavje dəkɑ̃tɛʁ]), better known as his stage name Tom Snare, is a French DJ and record producer from Dunkirk. Tom Snare rose to fame with a hit single, "Philosophy", with reached #2 in France in early 2006 and is now on the playlist of world famous DJs and bands such as Robbie Rivera, Global Deejays and Hi_Tack. Tom Snare have also released singles under other aliases, such as Blue Star, Pure Star, Master Of Sciences and Undertalk. Tom Snare's first album, Tom Snare's World, was released in October 2006.
```