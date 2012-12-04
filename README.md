git-pylint-commit-hook
======================

<a href='https://travis-ci.org/sebdah/git-pylint-commit-hook'><img src='https://secure.travis-ci.org/sebdah/git-pylint-commit-hook.png?branch=master'></a>

Pre-commit hook for Git checking Python code quality. The hook will check files ending with `.py` or that has a she bang containing `python`.

Set the threshold for the quality by updating the `LIMIT` value in the `pre-commit` hook.

Installation
------------

Download the hook (or just copy it from GitHub) and save it in your Git repo as `.git/hooks/pre-commit`.

Don't forget to make it executable.


Usage
------

The commit hook will automatically be called when you are running `git commit`. If you want to skip the tests for a certain commit, use the `-n` flag, `git commit -n`.

### Setting score limit

Open the `pre-commit` script and update the `LIMIT` value according to your needs. E.g.

	LIMIT = 8.0

### Custom `pylint` command line options

The hook supports custom command line options to be specified. Those can be added to the `PYLINT_PARAMS` inside the `pre-commit` script. E.g.

	PYLINT_PARAMS = '--rcfile=/path/to/project/pylint.rc'


Requirements
------------

This commit hook is written in Python and has the following requirements:

- [pylint](http://www.logilab.org/857) (`sudo pip install pylint`)
- Python >2.5 and <3.0


Release notes
-------------

### 0.6 (2012-12-04)

- Added support for [negative pylint scores #4](https://github.com/sebdah/git-pylint-commit-hook/issues/4)
- Added support for [custom command line params to pylint #6](https://github.com/sebdah/git-pylint-commit-hook/issues/6)
- Fixed bug [#3 Empty .py files fails according to pylint](https://github.com/sebdah/git-pylint-commit-hook/issues/3)

### 0.5 (2012-12-01)

- Fixed bug [#2 Hook missed some Python files when committing a mixture of file types](https://github.com/sebdah/git-pylint-commit-hook/issues/2)

### 0.4 (2012-11-30)

- Fixed bug [#1 Files parsed number is not increased](https://github.com/sebdah/git-pylint-commit-hook/issues/1)

### 0.3 (2012-11-18)

- Fixed bug with non-python files getting checked, if they contained `python` on the first row

### 0.2 (2012-11-16)

- Added support for handling moved or deleted files

### 0.1 (2012-11-09)

 - Initial release of the commit hook
