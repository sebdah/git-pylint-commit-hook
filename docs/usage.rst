Usage
=====

Basic configuration
-------------------

To use ``git-pylint-commit-hook`` in a project, create a new file under ``/project/root/.git/hooks/pre-commit`` and add the following to that file:
::

    #!/usr/bin/env bash
    git-pylint-commit-hook

Save the file and make it executable:
::

    chmod +x .git/hooks/pre-commit

Your Python files should now be checked upon commit.


Command line options
--------------------

The ``git-pylint-commit-hook`` can be configured using command line options. The command line options are:
::

      --limit LIMIT         Score limit, files with a lower score will stop the
                            commit. Default: 8.0
      --pylint PYLINT       Path to pylint executable. Default: pylint
      --pylintrc PYLINTRC   Path to pylintrc file. Options in the pylintrc will
                            override the command line parameters. Default:
                            pylintsearch order
      --pylint-params PYLINT_PARAMS
                            Custom pylint parameters to add to the pylint command
      --suppress-report     Suppress report output if pylint fails
      --always-show-violations
                            Show violations in case of pass as well
      --version             Print current version number
      --ignore IGNORED_FILES
                            Add regex to blacklist files or directories, allowing
                            to avoid running pylint those files.

You can simply append those to the command created in the **Basic configuration** above.


Support for ``.pylintrc`` files
-------------------------------

``git-pylint-commit-hook`` will automatically find your pylint configuration files, according to the pylint configuration file default read order. Any configuration found for the project will be used in the ``git-pylint-commit-hook``.

You can also define a custom pylint configuration file using the ``--pylintrc`` command line option.


Git configuration
^^^^^^^^^^^^^^^^^

Settings are loaded by default from the ``.pylintrc`` file in the root of your repo.
::

    [pre-commit-hook]
    command=custom_pylint
    params=--rcfile=/path/to/another/pylint.rc
    limit=8.0

``command`` is for the actual command, for instance if pylint is not installed globally, but is in a virtualenv inside the project itself.

``params`` lets you pass custom parameters to pylint

``limit`` is the lowest value which you want to allow for a pylint score.  Any lower than this, and the script will fail and won't commit.

Any of these can be bypassed directly in the pre-commit hook itself.  You can also set a different default place to look for the pylintrc file.
