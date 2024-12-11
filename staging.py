import os
import shutil
import hashlib
import json


class StagingArea:
    def __init__(self, staging_path, ignore_file_path):
        self.staging_path = staging_path
        self.ignore_file_path = ignore_file_path

    def _get_file_hash(self, file_path):
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _is_ignored(self, file_path):
        with open(self.ignore_file_path, 'r') as f:
            ignore_patterns = f.read().splitlines()
        filename = os.path.basename(file_path)
        return any(pattern in filename for pattern in ignore_patterns)

    def add(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if self._is_ignored(file_path):
            print(f"File {file_path} is ignored")
            return

        file_hash = self._get_file_hash(file_path)
        staged_file_path = os.path.join(self.staging_path, file_hash)
        shutil.copy2(file_path, staged_file_path)

        metadata = {'original_path': file_path, 'hash': file_hash}
        with open(os.path.join(self.staging_path, f'{file_hash}.json'), 'w') as f:
            json.dump(metadata, f)

        print(f"Added {file_path} to staging")
