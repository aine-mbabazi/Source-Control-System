import argparse
import sys
from repository import TrinaRepository
from staging import Staging
from commit import Commit
from branch import Branch
from diff import Diff

def create_cli():
    parser = argparse.ArgumentParser(description="Trina - Distributed Source Control System")
    subparsers = parser.add_subparsers(dest='command', help='Trina commands')

    # CLI command setups
    subparsers.add_parser('init', help='Initialize a new Trina repository').add_argument('path', nargs='?', default='.')
    subparsers.add_parser('add', help='Stage files for commit').add_argument('files', nargs='+')
    subparsers.add_parser('commit', help='Create a new commit').add_argument('-m', '--message', required=True)
    subparsers.add_parser('branch', help='Create a new branch').add_argument('branch_name')
    subparsers.add_parser('diff', help='Show differences between commits').add_argument('commit1').add_argument('commit2')

    args = parser.parse_args()
    repo = TrinaRepository('.')

    try:
        if args.command == 'init':
            print(f"Initialized Trina repository in {args.path}")
        elif args.command == 'add':
            staging = Staging(repo)
            for file in args.files:
                staging.add(file)
        elif args.command == 'commit':
            Commit(repo).commit(args.message)
        elif args.command == 'branch':
            Branch(repo).branch(args.branch_name)
        elif args.command == 'diff':
            Diff(repo).diff(args.commit1, args.commit2)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_cli()
