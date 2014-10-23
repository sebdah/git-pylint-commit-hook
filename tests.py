# pylint: disable=missing-docstring

import os
import shutil
import subprocess
import tempfile
import unittest

from git_pylint_commit_hook import commit_hook

class TestHook(unittest.TestCase):
    # pylint: disable=protected-access,too-many-public-methods,invalid-name

    def setUp(self):
        # Create temporary directory
        self.tmp_dir = tempfile.mkdtemp(prefix='pylint_hook_test_')

        # Set current working directory to the temporary directory for
        # all the commands run in the test
        os.chdir(self.tmp_dir)

        # Initialize temporary git repository
        self.cmd('git init')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def write_file(self, filename, contents):
        with open(os.path.join(self.tmp_dir, filename), 'w') as wfile:
            wfile.write(contents)
        return filename

    def cmd(self, args):
        return subprocess.check_output(args.split(), cwd=self.tmp_dir)

    def test_current_commit(self):
        """Test commit_hook._current_commit"""

        # Test empty tree
        empty_hash = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
        self.assertEquals(commit_hook._current_commit(), empty_hash)

        # Test after commit
        self.cmd('git commit --allow-empty -m msg')
        self.assertEquals(commit_hook._current_commit(), 'HEAD')

    def test_list_of_committed_files(self):
        """Test commit_hook._get_list_of_committed_files"""

        # Test empty tree
        self.assertEquals(commit_hook._get_list_of_committed_files(), [])

        # Create file 'a'
        a = self.write_file('a', 'foo')
        self.assertEquals(commit_hook._get_list_of_committed_files(), [])

        # Add 'a'
        self.cmd('git add ' + a)
        self.assertEquals(commit_hook._get_list_of_committed_files(), [a])

        # Commit 'a'
        self.cmd('git commit -m msg')
        self.assertEquals(commit_hook._get_list_of_committed_files(), [])

        # Edit 'a'
        self.write_file('a', 'bar')
        self.assertEquals(commit_hook._get_list_of_committed_files(), [])

        # Add 'a'
        self.cmd('git add ' + a)
        self.assertEquals(commit_hook._get_list_of_committed_files(), [a])

    def test_is_python_file(self):
        """Test commit_hook._is_python_file"""

        # Extension
        a = self.write_file('a.py', '')
        self.assertTrue(commit_hook._is_python_file(a))

        # Empty
        a = self.write_file('b', '')
        self.assertFalse(commit_hook._is_python_file(a))

        # Shebang
        self.write_file('b', '#!/usr/bin/env python')
        self.assertTrue(commit_hook._is_python_file(a))

    def test_parse_score(self):
        """Test commit_hook._parse_score"""

        text = 'Your code has been rated at 8.51/10'
        self.assertEquals(commit_hook._parse_score(text), 8.51)

        text = 'Your code has been rated at 8.51'
        self.assertEquals(commit_hook._parse_score(text), 0.0)
