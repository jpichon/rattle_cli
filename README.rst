What is this?
-------------

This is a command-line script to gather reading statistics on the
language of the books read, based on the user's Goodreads reviews. If
you read in multiple languages, maybe you'd like to make sure you're
reading more or less equally in each language so that your skills in
one don't atrophy too much.

Usage
-----

When running the script, you'll be asked to authorise the application
to collect your review data, then your statistics for the specified
year will be displayed. As an example:

::

    $ python rattle-cli.py --lang en fr ja --year 2016
    Books read based on Goodreads reviews
    en: 3
    fr: 1
    ja: 2

You can also see the detailed version.

::

    $ python rattle-cli.py --lang en fr ja --year 2016 --details
    Books read based on Goodreads reviews
    en: 3
    The Hero of Ages (Mistborn, #3), by Brandon Sanderson
    The Well of Ascension (Mistborn, #2), by Brandon Sanderson
    The Final Empire (Mistborn, #1), by Brandon Sanderson

    fr: 1
    Vol de nuit, by Antoine de Saint-Exupéry

    ja: 2
    探偵ガリレオ [Tantei Garireo] (ガリレオ, #1), by Keigo Higashino
    陽気なギャングが地球を回す, by Kotaro Isaka

Let's say that like me you don't actually have a special shelf for
books in English, because that's the default language you read in. In
other words: if a book isn't shelved on either 'fr' or 'ja' then it's
fair to assume it's in English.

::

    $ python rattle-cli.py --lang fr ja --other --year 2016
    Books read based on Goodreads reviews
    default: 3
    fr: 1
    ja: 2


Getting started
---------------

Install the requirements:

::

    $ pip install -r requirements.txt


Create a ``secrets.py`` file (at the same level as ``rattle_cli.py``)
set with the following variables:

::

    api_key = "Reading"
    api_secret = "All The Things"

You can get an API key and secret by logging into your Goodreads
account and browing to https://www.goodreads.com/api/keys (you can put
in bogus information, as long as you don't make lots and lots of call
the Goodreads folks don't mind).

The first time you use the app, you'll have to authorise it:

::

  $ python rattle_cli.py --languages en de --year 2016
  Visit this URL in your browser: https://www.goodreads.com/oauth/authorize?oauth_token=abcdefz
  Have you authorized me? (y/n)

Open the URL in the browser. Once you've allowed the app, you can
return to the CLI and type in ``y``. If it worked, you'll have to wait a
little while your reviews are being fetched then the stats will be
displayed.

::

  $ python rattle_cli.py --languages en de --year 2016
  Visit this URL in your browser: https://www.goodreads.com/oauth/authorize?oauth_token=abcdefz
  Have you authorized me? (y/n) y
  Books read based on Goodreads reviews
  en: 23
  de: 17

The access token and access token secrets will be stored in a
``.access_token`` file so you won't have to reauthorise next time. If
there's ever authentication issues or 401 errors, you might want to
delete that file and reauthorise the app again.

Versions
--------

Tested with Python 3.3.

::

    $ python rattle-cli.py --help

Known issues
------------

If one retrieves the individual book details for a specific id, there
is a language_code attribute present. I used shelves instead of this
for a number of reasons:

  - It matches my own shelving system.

  - Not every book on Goodreads is associated with a language code,
    particularly older/less popular books. Sure, you could update
    Goodreads as you find issues but only Librarians can do that, so
    you'd need to apply and be approved for the role first, which
    isn't guaranteed.

  - The current system uses the user reviews list API, which takes
    only a few API calls to get through a user's entire list of
    books. Getting each book's details would take much longer, and in
    that case it'd probably be smarter to store the data in a database
    and make sure to only get the updated stuff (new books, modified
    read dates) afterward instead. Maybe someday. There are other cool
    stats the data could be used for.
