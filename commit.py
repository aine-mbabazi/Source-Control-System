import os
import json
import shutil
import hashlib
import pickle


class CommitManager:
    def __init__(self, commits_path, staging_path, branches_path, current_branch):
        self.commits_path = commits_path
        self.staging_path = staging_path
        self.branches_path = branches_path
        self.current_branch = current_branch

    def commit(self, message):
        staged_files = [f for f in os.listdir(self.staging_path) if f.endswith('.json')]
        if not staged_files:
            print("No changes to commit")
            return

        commit_hash = hashlib.sha256(message.encode()).hexdigest()[:8]
        commit_path = os.path.join(self.commits_path, commit_hash)
        os.makedirs(commit_path)

        for metadata_file in staged_files:
            metadata_path = os.path.join(self.staging_path, metadata_file)
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            staged_file_path = os.path.join(self.staging_path, metadata['hash'])
            dest_file_path = os.path.join(commit_path, os.path.basename(metadata['original_path']))
            shutil.copy2(staged_file_path, dest_file_path)

        commit_metadata = {
            'message': message,
            'files': [json.load(open(os.path.join(self.staging_path, f)))['original_path'] for f in staged_files]
        }
        with open(os.path.join(commit_path, 'commit_info.json'), 'w') as f:
            json.dump(commit_metadata, f)

        branch_path = os.path.join(self.branches_path, self.current_branch)
        with open(branch_path, 'rb') as f:
            commits = pickle.load(f)
        commits.append(commit_hash)

        with open(branch_path, 'wb') as f:
            pickle.dump(commits, f)

        for file in os.listdir(self.staging_path):
            os.remove(os.path.join(self.staging_path, file))

        print(f"Committed {len(staged_files)} files with message: {message}")
