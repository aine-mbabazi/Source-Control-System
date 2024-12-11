import hashlib
import unittest
import os
import tempfile
import shutil
from repository import TrinaRepository

class TestTrinaRepository(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo = TrinaRepository(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        self.assertTrue(os.path.isdir(self.repo.repo_path))
        self.assertTrue(os.path.isdir(self.repo.staging_path))
        self.assertTrue(os.path.isdir(self.repo.commits_path))
        self.assertTrue(os.path.isdir(self.repo.branches_path))

    def test_add_existing_file(self):
        file_path = os.path.join(self.test_dir, 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        self.repo.add(file_path)
        staged_file = os.path.join(self.repo.staging_path, self.repo._get_file_hash(file_path))
        self.assertTrue(os.path.isfile(staged_file))

    def test_add_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.repo.add('non_existent.txt')

    def test_commit_with_files(self):
        file_path = os.path.join(self.test_dir, 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        self.repo.add(file_path)
        self.repo.commit('Test commit')
        commit_hash = hashlib.sha256('Test commit'.encode()).hexdigest()[:8]
        commit_dir = os.path.join(self.repo.commits_path, commit_hash)
        self.assertTrue(os.path.isdir(commit_dir))
        self.assertTrue(os.path.isfile(os.path.join(commit_dir, 'commit_info.json')))

    def test_commit_without_files(self):
        with self.assertRaises(Exception) as cm:
            self.repo.commit('Test commit')
        self.assertEqual(str(cm.exception), "No changes to commit")

    def test_commit_with_empty_message(self):
        file_path = os.path.join(self.test_dir, 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        self.repo.add(file_path)
        with self.assertRaises(Exception) as cm:
            self.repo.commit('')
        self.assertEqual(str(cm.exception), "Commit message cannot be empty")

    def test_log(self):
        file_path = os.path.join(self.test_dir, 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        self.repo.add(file_path)
        self.repo.commit('First commit')
        log_output = self.repo.log()
        self.assertIn('First commit', log_output)

    def test_log_no_commits(self):
        log_output = self.repo.log()
        self.assertEqual(log_output, "No commits to display")

    def test_branch_creation(self):
        self.repo.branch('new_branch')
        self.assertTrue(os.path.exists(os.path.join(self.repo.branches_path, 'new_branch')))

    def test_branch_creation_invalid_name(self):
        with self.assertRaises(ValueError) as cm:
            self.repo.branch('')
        self.assertEqual(str(cm.exception), "Invalid branch name")

    def test_diff(self):
        file_path1 = os.path.join(self.test_dir, 'testfile1.txt')
        file_path2 = os.path.join(self.test_dir, 'testfile2.txt')
        with open(file_path1, 'w') as f1, open(file_path2, 'w') as f2:
            f1.write('line 1\nline 2')
            f2.write('line 1\nline 2\nline 3')
        self.repo.add(file_path1)
        self.repo.commit('First commit')
        self.repo.add(file_path2)
        self.repo.commit('Second commit')

        commit_hashes = os.listdir(self.repo.commits_path)
        commit1 = commit_hashes[-2]
        commit2 = commit_hashes[-1]

        diff_output = self.repo.diff(commit1, commit2)
        self.assertIn('line 3', diff_output)

    def test_diff_non_existent_commits(self):
        with self.assertRaises(Exception) as cm:
            self.repo.diff('nonexistent1', 'nonexistent2')
        self.assertEqual(str(cm.exception), "One or both of the specified commits do not exist")

    def test_diff_no_changes(self):
        file_path = os.path.join(self.test_dir, 'testfile.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        self.repo.add(file_path)
        self.repo.commit('First commit')
        commit_hash = hashlib.sha256('First commit'.encode()).hexdigest()[:8]
        diff_output = self.repo.diff(commit_hash, commit_hash)
        self.assertEqual(diff_output, "No differences")

    def test_clone(self):
        clone_dir = os.path.join(self.test_dir, 'clone')
        self.repo.clone(clone_dir)
        self.assertTrue(os.path.isdir(os.path.join(clone_dir, '.trina')))

    def test_clone_invalid_path(self):
        with self.assertRaises(Exception) as cm:
            self.repo.clone('/invalid/path')
        self.assertEqual(str(cm.exception), "Destination path does not exist")

    def test_ignore(self):
        self.repo.ignore('*.txt')
        with open(self.repo.ignore_file_path, 'r') as f:
            ignore_patterns = f.read().splitlines()
        self.assertIn('*.txt', ignore_patterns)

    def test_ignore_invalid_pattern(self):
        with self.assertRaises(ValueError) as cm:
            self.repo.ignore('')
        self.assertEqual(str(cm.exception), "Invalid ignore pattern")

if __name__ == '__main__':
    unittest.main()
