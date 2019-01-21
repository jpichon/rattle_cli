.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/jpichon/rattle_cli/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

rattle_cli could always use more documentation, whether as part of the official
rattle_cli docs, in docstrings, or even on the web in blog posts, articles, and
such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/jpichon/rattle_cli/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `rattle_cli` for local development.

1. Fork the `rattle_cli` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/rattle_cli.git

3. Install your local copy into a virtualenv. For example::

    $ virtualenv --no-site-packages .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt -r test-requirements.txt

   Make sure the virtualenv is set up with Python 3. If the default on your
   system uses Python 2, you can explicity specify the path to your Python 3
   binaries. For example::

   $ virtualenv --no-site-packages --python /usr/bin/python3 .venv

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 rattle_cli
    $ nosetests
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for Python 3.4 to 3.7. Check
   https://travis-ci.org/jpichon/rattle_cli/pull_requests and make sure that
   the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ nosetests rattle_cli.tests.test_goodreads
