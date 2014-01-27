""" Commit hook for pylint """

import os
import re
import sys
import subprocess
import ConfigParser


def _get_list_of_committed_files():
    """ Returns a list of files about to be commited. """
    files = []
    # pylint: disable=E1103
    output = subprocess.check_output(
        'git diff-index --cached HEAD'.split())
    for result in output.split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ['A', 'M']:
                files.append(result[5])

    return files


def check_repo(
        limit, pylint='pylint', pylintrc='.pylintrc', pylint_params=None):
    """ Main function doing the checks

    :type limit: float
    :param limit: Minimum score to pass the commit
    :type pylint: str
    :param pylint: Path to pylint executable
    :type pylintrc: str
    :param pylintrc: Path to pylintrc file
    :type pylint_params: str
    :param pylint_params: Custom pylint parameters to add to the pylint command
    """
    # List of checked files and their results
    python_files = []

    # Set the exit code
    all_filed_passed = True

    # Find Python files
    for filename in _get_list_of_committed_files():
        # Check the file extension
        if filename[-3:] == '.py':
            python_files.append((filename, None))
            continue

        # Check the first line for a python shebang
        try:
            with open(filename, 'r') as file_handle:
                first_line = file_handle.readline()
            if 'python' in first_line and '#!' in first_line:
                python_files.append((filename, None))
        except IOError:
            print 'File not found (probably deleted): {}\t\tSKIPPED'.format(
                filename)

    # Don't do anything if there are no Python files
    if len(python_files) == 0:
        sys.exit(0)

    # Load any pre-commit-hooks options from a .pylintrc file (if there is one)
    if os.path.exists(pylintrc):
        conf = ConfigParser.SafeConfigParser()
        conf.read(pylintrc)
        if conf.has_option('pre-commit-hook', 'command'):
            pylint = conf.get('pre-commit-hook', 'command')
        if conf.has_option('pre-commit-hook', 'params'):
            pylint_params += ' ' + conf.get('pre-commit-hook', 'params')
        if conf.has_option('pre-commit-hook', 'limit'):
            limit = float(conf.get('pre-commit-hook', 'limit'))

    # Pylint Python files
    i = 1
    regexp = re.compile(r'^Your\ code\ has\ been\ rated\ at\ (\-?[0-9\.]+)/10')
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

        # Set the initial score
        score = 0.00

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

            command.append(python_file)

            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, _ = proc.communicate()
        except OSError:
            print("\nAn error occurred. Is pylint installed?")
            sys.exit(1)

        # Check for the result
        # pylint: disable=E1103
        for line in out.split('\n'):
            match = re.match(regexp, line)
            if match:
                score = float(match.group(1))

        # Verify the score
        if score >= float(limit):
            status = 'PASSED'
        else:
            status = 'FAILED'
            all_filed_passed = False

        # Add some output
        print('{:.2}/10.00\t{}'.format(score, status))

        # Bump parsed files
        i += 1

    return all_filed_passed
