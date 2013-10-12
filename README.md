git-pylint-commit-hook
======================

<a href='https://travis-ci.org/sebdah/git-pylint-commit-hook'><img src='https://secure.travis-ci.org/sebdah/git-pylint-commit-hook.png?branch=master'></a>

Pre-commit hook for Git checking Python code quality. The hook will check files ending with `.py` or that has a she bang (#!) containing `python`.

By default the script looks in the root directory of your project for a .pylintrc file, which it passes to pylint.  It also looks for a [pre-commit-hook] section for options of it's own.

Installation
------------

Download the hook (or just copy it from GitHub) and save it in your Git repo as `.git/hooks/pre-commit`.

Don't forget to make it executable.


Usage
------

The commit hook will automatically be called when you are running `git commit`. If you want to skip the tests for a certain commit, use the `-n` flag, `git commit -n`.

### Configuration

Settings are loaded by default from the .pylintrc file in the root of your repo.

    [pre-commit-hook]
    command=custom_pylint
    params=--rcfile=/path/to/another/pylint.rc
    limit=8.0

_command_ is for the actual command, for instance if pylint is not installed globally, but is in a virtualenv inside the project itself.

_params_ lets you pass custom parameters to pylint

_limit_ is the lowest value which you want to allow for a pylint score.  Any lower than this, and the script will fail and won't commit.

Any of these can be bypassed directly in the pre-commit hook itself.  You can also set a different default place to look for the pylintrc file.

Requirements
------------

This commit hook is written in Python and has the following requirements:

- [pylint](http://www.logilab.org/857) (`sudo pip install pylint`)
- Python >2.5 and <3.0


Release notes
-------------

### ???

- Added support for default .pylintrc file, and also for loading our own options from there.

### 0.8 (2013-01-09)

- Fixed bug [#9 Old file names of moved files are checked](https://github.com/sebdah/git-pylint-commit-hook/issues/9)

### 0.7 (2012-12-07)

- Bug when skipping __init__.py files fixed. Wrong path was checked under some circumstanses

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
