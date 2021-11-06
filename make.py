#! /bin/python3

from argparse_helper import initialize_command_line_interface, get_command_line_args
from project_targets import get_project_targets

def main():
    # Start the CLI and parse any command line values/flags
    initialize_command_line_interface()
    args = get_command_line_args()

    # Create dictionary of project targets; the default value includes all defined targets
    targets = get_project_targets()

    # Overwrite target dictionary if only one target was selected on the command line
    if args.target != 'all':
        if args.target not in targets:
            raise ValueError("{0} not a valid target.".format(args.target))
        else:
            targets = { args.target:targets[args.target] }

    # For all targets in the target dictionary (either all targets or just the one specified),
    # execute the desired command (clean, purify, zip, or build)
    for target in targets:
        targets[target].execute(args.execute, args.verbose)
    
if __name__ == "__main__":
    main()
