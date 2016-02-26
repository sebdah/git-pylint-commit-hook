# pylint: disable=missing-docstring

import os
import shutil
import subprocess
import tempfile
import unittest

from git_pylint_commit_hook import commit_hook


class TestException(Exception):
    pass


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

    def test_current_stash(self):
        """Test commit_hook._current_stash"""

        # Test empty stash
        empty_hash = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
        self.assertEquals(commit_hook._current_stash(), empty_hash)

        # Need an initial commit to stash
        self.cmd('git commit --allow-empty -m msg')

        # Test after stash
        self.write_file('a', 'foo')
        self.cmd('git stash --include-untracked')
        stash = commit_hook._current_stash()
        self.assertNotEquals(stash, empty_hash)

        # Test the next stash doesn't look like the last
        self.write_file('b', 'bar')
        self.cmd('git stash --include-untracked')
        self.assertNotEquals(commit_hook._current_stash(), stash)

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

    def test_stash_unstaged(self):
        """Test commit_hook._stash_unstaged"""

        # git stash doesn't work without an initial commit :(
        self.cmd('git commit --allow-empty -m msg')

        # Write a file with a style error
        a = self.write_file('a', 'style error!')
        # Add it to the repository
        self.cmd('git add ' + a)

        # Fix the style error but don't add it
        self.write_file('a', 'much better :)')

        # Stash any unstaged changes; check the unstaged changes disappear
        with commit_hook._stash_unstaged():
            with open(a) as f:
                self.assertEquals(f.read(), 'style error!')

        # Check the unstaged changes return
        with open(a) as f:
            self.assertEquals(f.read(), 'much better :)')

        # Stash changes then pretend we crashed
        with self.assertRaises(TestException):
            with commit_hook._stash_unstaged():
                raise TestException

        # Check the unstaged changes return
        with open(a) as f:
            self.assertEquals(f.read(), 'much better :)')

    def test_stash_unstaged_untracked(self):
        """Test commit_hook._stash_unstaged leaves untracked files alone"""

        # git stash doesn't work without an initial commit :(
        self.cmd('git commit --allow-empty -m msg')

        # Write a file but don't add it
        a = self.write_file('a', 'untracked')

        # Stash changes; check nothing happened
        with commit_hook._stash_unstaged():
            with open(a) as f:
                self.assertEqual(f.read(), 'untracked')

        # Check the file is still unmodified
        with open(a) as f:
            self.assertEquals(f.read(), 'untracked')

    def test_stash_unstaged_no_initial(self):
        """Test commit_hook._stash_unstaged handles no initial commit"""

        # Write a file with a style error
        a = self.write_file('a', 'style error!')
        # Add it to the repository
        self.cmd('git add ' + a)

        # Fix the style error but don't add it
        self.write_file('a', 'much better :)')

        # A warning should be printed to screen saying nothing is stashed
        with commit_hook._stash_unstaged():
            with open(a) as f:
                self.assertEquals(f.read(), 'much better :)')

        # Check the file is still unmodified
        with open(a) as f:
            self.assertEquals(f.read(), 'much better :)')
