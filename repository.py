import os
import pickle


class TrinaRepository:
    def __init__(self, path='.'):
        self.repo_path = os.path.join(path, '.trina')
        self.staging_path = os.path.join(self.repo_path, 'staged')
        self.commits_path = os.path.join(self.repo_path, 'commits')
        self.branches_path = os.path.join(self.repo_path, 'branches')
        self.ignore_file_path = os.path.join(self.repo_path, 'ignore.txt')

        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            os.makedirs(self.staging_path)
            os.makedirs(self.commits_path)
            os.makedirs(self.branches_path)

            with open(os.path.join(self.branches_path, 'main'), 'wb') as f:
                pickle.dump([], f)

            with open(self.ignore_file_path, 'w') as f:
                f.write('.trina\n')

        self.current_branch = 'main'
