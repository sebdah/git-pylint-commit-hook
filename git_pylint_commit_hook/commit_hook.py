""" Commit hook for pylint """
import decimal
import os
import re
import sys
import subprocess
import collections
import configparser
import contextlib

ExecutionResult = collections.namedtuple(
    'ExecutionResult',
    'status, stdout, stderr'
)

def _futurize_str(obj):
    if isinstance(obj, bytes):
        obj = obj.decode('utf-8')
    return obj


def _execute(cmd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    status = process.poll()
    return ExecutionResult(status, stdout, stderr)


def _current_commit():
    if _execute('git rev-parse --verify HEAD'.split()).status:
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    else:
        return 'HEAD'


def _current_stash():
    res = _execute('git rev-parse -q --verify refs/stash'.split())
    if res.status:
        # not really as meaningful for a stash, but makes some sense
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    else:
        return res.stdout


def _get_list_of_committed_files():
    """ Returns a list of files about to be commited. """
    files = []
    # pylint: disable=E1103
    diff_index_cmd = 'git diff-index --cached %s' % _current_commit()
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in _futurize_str(output).split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ['A', 'M']:
                files.append(result[5])

    return files


def _is_python_file(filename):
    """Check if the input file looks like a Python script

    Returns True if the filename ends in ".py" or if the first line
    contains "python" and "#!", returns False otherwise.

    """
    if filename.endswith('.py'):
        return True
    else:
        with open(filename, 'r') as file_handle:
            first_line = file_handle.readline()
        return 'python' in first_line and '#!' in first_line


_SCORE_REGEXP = re.compile(
    r'^Your\ code\ has\ been\ rated\ at\ (\-?[0-9\.]+)/10')


def _parse_score(pylint_output):
    """Parse the score out of pylint's output as a float

    If the score is not found, return 0.0.

    """
    for line in pylint_output.splitlines():
        match = re.match(_SCORE_REGEXP, _futurize_str(line))
        if match:
            return float(match.group(1))
    return 0.0


@contextlib.contextmanager
def _stash_unstaged():
    """Stashes any changes on entry and restores them on exit.

    If there is no initial commit, print a warning and do nothing.

    """
    if _current_commit() != 'HEAD':
        # git stash doesn't work with no initial commit, so warn and do nothing
        print('WARNING: unable to stash changes with no initial commit')
        yield
        return

    # git stash still returns 0 if there is nothing to stash,
    # so inspect the current stash before and after saving
    original_stash = _current_stash()
    # leave a message marking the stash as ours in case something goes wrong
    # so that the user can work out what happened and fix things manually
    subprocess.check_call('git stash save -q --keep-index '
                          'git-pylint-commit-hook'.split())
    new_stash = _current_stash()

    try:
        # let the caller do whatever they wanted to do
        # (but we still want to restore the tree if an exception was thrown)
        yield
    finally:
        # only restore if we actually stashed something
        if original_stash != new_stash:
            # avoid merge issues
            subprocess.check_call('git reset --hard -q'.split())
            # restore everything to how it was
            subprocess.check_call('git stash pop --index -q'.split())


def check_repo(
        limit, pylint='pylint', pylintrc='.pylintrc', pylint_params='',
        suppress_report=False):
    """ Main function doing the checks

    :type limit: float
    :param limit: Minimum score to pass the commit
    :type pylint: str
    :param pylint: Path to pylint executable
    :type pylintrc: str
    :param pylintrc: Path to pylintrc file
    :type pylint_params: str
    :param pylint_params: Custom pylint parameters to add to the pylint command
    :type suppress_report: bool
    :param suppress_report: Suppress report if score is below limit
    """
    # List of checked files and their results
    python_files = []

    # Set the exit code
    all_filed_passed = True

    # Stash any unstaged changes while we look at the tree
    with _stash_unstaged():
        # Find Python files
        for filename in _get_list_of_committed_files():
            try:
                if _is_python_file(filename):
                    python_files.append((filename, None))
            except IOError:
                print('File not found (probably deleted): {}\t\tSKIPPED'.format(
                    filename))

        # Don't do anything if there are no Python files
        if len(python_files) == 0:
            sys.exit(0)

        # Load any pre-commit-hooks options from a .pylintrc file (if there is one)
        if os.path.exists(pylintrc):
            conf = configparser.SafeConfigParser()
            conf.read(pylintrc)
            if conf.has_option('pre-commit-hook', 'command'):
                pylint = conf.get('pre-commit-hook', 'command')
            if conf.has_option('pre-commit-hook', 'params'):
                pylint_params += ' ' + conf.get('pre-commit-hook', 'params')
            if conf.has_option('pre-commit-hook', 'limit'):
                limit = float(conf.get('pre-commit-hook', 'limit'))

        # Pylint Python files
        i = 1
        for python_file, score in python_files:
            # Allow __init__.py files to be completely empty
            if os.path.basename(python_file) == '__init__.py':
                if os.stat(python_file).st_size == 0:
                    print(
                        'Skipping pylint on {} (empty __init__.py)..'
                        '\tSKIPPED'.format(python_file))

                    # Bump parsed files
                    i += 1
                    continue

            # Start pylinting
            sys.stdout.write("Running pylint on {} (file {}/{})..\t".format(
                python_file, i, len(python_files)))
            sys.stdout.flush()
            try:
                command = [pylint]
                if pylint_params:
                    command += pylint_params.split()
                    if '--rcfile' not in pylint_params:
                        command.append('--rcfile={}'.format(pylintrc))
                else:
                    command.append('--rcfile={}'.format(pylintrc))

                command.append(python_file)
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

                out, _ = proc.communicate()
            except OSError:
                print("\nAn error occurred. Is pylint installed?")
                sys.exit(1)

            # Verify the score
            score = _parse_score(out)
            if score >= float(limit):
                status = 'PASSED'
            else:
                status = 'FAILED'
                all_filed_passed = False

            # Add some output
            print('{:.2}/10.00\t{}'.format(decimal.Decimal(score), status))
            if 'FAILED' in status:
                if suppress_report:
                    command.append('--reports=n')
                    proc = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    out, _ = proc.communicate()
                print(_futurize_str(out))


            # Bump parsed files
            i += 1

    return all_filed_passed
