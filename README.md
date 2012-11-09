git-pylint-commit-hook
======================

Pre-commit hook for Git checking Python code quality.

Installation
------------

Download the hook (or just copy it from GitHub) and save it in your Git repo as `.git/hooks/pre-commit`.

Don't forget to make it executable.

Requirements
------------

This commit hook is written in Python and has the following requirements:

- [pylint](http://www.logilab.org/857)
- Python >2.5