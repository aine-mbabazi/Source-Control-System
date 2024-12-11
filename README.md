# Trina - Distributed Version Control System

Trina is a lightweight, Git-inspired version control system implemented in Python.

## Features

- Initialize repositories
- Stage and commit files
- Create branches
- View commit history
- Compare commits
- Clone repositories
- Ignore files

## Installation

```bash
# Clone the repository
git clone https://github.com/aine-mbabazi/Source-Control-System
cd trina

# Install in editable mode
pip install -e .
```

## Usage

### Initialize a Repository

```bash
trina init
```

### Stage Files

```bash
trina add file1.txt file2.txt
```

### Commit Changes

```bash
trina commit -m "Initial commit message"
```

### Create a Branch

```bash
trina branch feature-branch
```

### View Commit History

```bash
trina log
```

### Ignore Files

```bash
trina ignore .env *.log node_modules
```

## Requirements

- Python 3.7+
- No external dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.