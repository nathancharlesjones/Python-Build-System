#! /bin/python3

from argparse_helper import initialize_command_line_interface, get_command_line_args
from project_targets import get_project_targets

# TODO: Add more comments

def main():
    initialize_command_line_interface()
    args = get_command_line_args()

    targets = get_project_targets()

    if args.target != 'all':
        if args.target not in targets:
            raise ValueError("{0} not a valid target.".format(args.target))
        else:
            targets = { args.target:targets[args.target] }

    for target in targets:
        if args.execute == 'clean':
            targets[target].clean(args.verbose)
        elif args.execute == 'purify':
            targets[target].purify(args.verbose)
        elif args.execute == 'zip':
            targets[target].zip(args.verbose)
        else:
            targets[target].build(args.verbose)
    
    # TODO: Add zip commands
    # TODO: Add checks to only build if dependency is newer than target
    #    - How to check for libraries/local dependencies?
    #    - Also create and check .d files
    
if __name__ == "__main__":
    main()
