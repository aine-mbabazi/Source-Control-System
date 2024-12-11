import os
import difflib


class DiffViewer:
    def __init__(self, commits_path):
        self.commits_path = commits_path

    def diff(self, commit1, commit2):
        commit1_path = os.path.join(self.commits_path, commit1)
        commit2_path = os.path.join(self.commits_path, commit2)

        commit1_files = os.listdir(commit1_path)
        commit2_files = os.listdir(commit2_path)

        for file in set(commit1_files + commit2_files):
            file1_path = os.path.join(commit1_path, file)
            file2_path = os.path.join(commit2_path, file)

            if not os.path.exists(file1_path) or not os.path.exists(file2_path):
                print(f"File {file} not present in one of the commits")
                continue

            with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
                diff = list(difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=f"a/{file}", tofile=f"b/{file}"))
                if diff:
                    print(f"Differences in {file}:")
                    print(''.join(diff))
