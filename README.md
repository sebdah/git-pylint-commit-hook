
git-pylint-commit-hook
======================

<a href='https://travis-ci.org/sebdah/git-pylint-commit-hook'><img src='https://secure.travis-ci.org/sebdah/git-pylint-commit-hook.png?branch=master'></a>

Pre-commit hook for Git checking Python code quality. The hook will check files ending with `.py` or that has a she bang (#!) containing `python`.

The script will try to find pylint configuration files in the order determined by pylint. It also looks for a [pre-commit-hook] section in the pylint configuration for commit hook specific options.

Installation
------------

Install via PyPI

    pip install git-pylint-commit-hook


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

Running tests
-------------

The test suite requires `nose2` to be installed. Install it with `pip install nose2`, then run the tests by executing the following command (in the project root folder):

    nose2

Requirements
------------

This project supports Python 2.7 and Python 3.5. Please install other requirements via

	pip install -r requirements.txt


Release notes
-------------

### 2.4.0 (2018-03-12)
- Skip `pylintrc` parameter, if file not present [#62](https://github.com/sebdah/git-pylint-commit-hook/issues/62)

### 2.3.0 (2018-02-24)
- Make stashing optional [#56](https://github.com/sebdah/git-pylint-commit-hook/pull/56)
- Bug fix for pylinit 1.7.x [#57](https://github.com/sebdah/git-pylint-commit-hook/pull/57)

### 2.2.2 (2017-05-19)
- Let the wrapper script call `sys.exit` [#55](https://github.com/sebdah/git-pylint-commit-hook/pull/55) contributed by [coldnight](https://github.com/coldnight)

### 2.2.1 (2016-09-27)
- [Correct index.lock file deletion and other fixes & formatting](https://github.com/sebdah/git-pylint-commit-hook/pull/52). Thanks to [@sandipagarwal](https://github.com/sandipagarwal) for this bug fix

### 2.2.0 (2016-09-08)
- Add support for Python 3.5
- [Support for showing pylint violations in case of passing of limit](https://github.com/sebdah/git-pylint-commit-hook/pull/48). Contributed by [@sandipagarwal](https://github.com/sandipagarwal)
- [Use pylints config file read order](https://github.com/sebdah/git-pylint-commit-hook/pull/39). Contributed by [@evanunderscore](https://github.com/evanunderscore)
- [Fix multiple git process problem](https://github.com/sebdah/git-pylint-commit-hook/pull/51). Thank you [@lagelalegal](https://github.com/lagelalegal) for providing a fix.
- [Add flag for ignoring certain files](https://github.com/sebdah/git-pylint-commit-hook/pull/41). Thanks [@thiblahute](https://github.com/thiblahute) for the contribution
- Some refactor and bug fixes

### 2.1.1 (2016-02-26)

- [Stash unstaged changes before running pylint](https://github.com/sebdah/git-pylint-commit-hook/pull/37). Thanks [@evanunderscore](https://github.com/evanunderscore) for the PR

### 2.1.0 (2016-01-18)

- [Add Python 3 support](https://github.com/sebdah/git-pylint-commit-hook/pull/40). Thanks [@jAlpedrinha](https://github.com/jAlpedrinha) for the PR
- [Add tox support](https://github.com/sebdah/git-pylint-commit-hook/pull/40). Thanks [@jAlpedrinha](https://github.com/jAlpedrinha) for the PR

### 2.0.9 (2014-10-16)

- [Add option to suppress pylint report if score is below limit](https://github.com/sebdah/git-pylint-commit-hook/pull/35). Thanks [@jwkvam](https://github.com/jwkvam) for the PR

### 2.0.7 (2014-10-16)

- [2.0.6 fails if pylint params is not set](https://github.com/sebdah/git-pylint-commit-hook/pull/31)
- [Separate code for testing if a file is Python into a new function](https://github.com/sebdah/git-pylint-commit-hook/pull/30)
- [Add unit tests for `_current_commit` and `get_list_of_committed_files`](https://github.com/sebdah/git-pylint-commit-hook/pull/29)

### 2.0.5 (2014-10-08)

- [--rcfile=.pylintrc is not added if pylint params is None](https://github.com/sebdah/git-pylint-commit-hook/pull/27)

### 2.0.5 (2014-05-06)

- [Make hook work properly on initial commit](https://github.com/sebdah/git-pylint-commit-hook/pull/25). Thanks [@evvers](https://github.com/evvers) for the PR

### 2.0.4 (2014-05-01)

- [Add pylint to install_requires](https://github.com/sebdah/git-pylint-commit-hook/pull/24). Thanks [@evvers](https://github.com/evvers) for the PR

### 2.0.3 (2014-02-07)

- Fixed error in decimal representation

### 2.0.1 (2013-12-08)

- [Added `--version` flag to command line #22](https://github.com/sebdah/git-pylint-commit-hook/issues/22)
- Packaging fixes

### 2.0.0 (2013-12-08)

- Documentation updated and moved to [Read The Docs](http://git-pylint-commit-hook.readthedocs.org/)
- `git-pylint-commit-hook` is now a regular command
- Installation via PyPI: `pip install git-pylint-commit-hook`
- Configurable using command line parameters. See the [documentation](http://git-pylint-commit-hook.readthedocs.org/) for details

### 1.0.0 (2013-10-13)

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
