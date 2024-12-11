import os
import pickle


class BranchManager:
    def __init__(self, branches_path, current_branch):
        self.branches_path = branches_path
        self.current_branch = current_branch

    def branch(self, branch_name):
        current_branch_path = os.path.join(self.branches_path, self.current_branch)
        new_branch_path = os.path.join(self.branches_path, branch_name)

        with open(current_branch_path, 'rb') as f:
            current_commits = pickle.load(f)

        with open(new_branch_path, 'wb') as f:
            pickle.dump(current_commits, f)

        print(f"Created new branch: {branch_name}")
