What is this?
-------------

This is a command-line script to gather reading statistics on the
language of the books read, based on the user's Goodreads reviews. If
you read in multiple languages, maybe you'd like to make sure you're
reading more or less equally in each language so that your skills in
one don't atrophy too much.

When running the script, you'll be asked to authorise the application
to collect your review data, then your statistics for the current year
(or whatever year is specified) will be displayed. As an example:

::

    $ python rattle-cli.py
    Books read based on Goodreads reviews
    en: 3
    fr: 1
    ja: 2

You can also see the detailed version.

::

    $ python rattle-cli.py
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

Installing requirements
-----------------------

Install the requirements:

::

    $ pip install -r requirements.txt


Set up the secrets.py file with the following variables:

::

    api_key = "Reading"
    api_secret = "All"
    access_token = "The"
    access_token_secret = "Things"

You can get an API key and secret by logging into your Goodreads
account and browing to https://www.goodreads.com/api/keys (you can put
in bogus information, as long as you don't make lots and lots of call
the Goodreads folks don't mind). For the access token, er, I'll add
the stuff to get it later.

Using
-----

Tested with Python 3.3.

::

    $ python rattle-cli.py
