import argparse

parser = None

def initialize_command_line_interface():
    global parser
    parser = argparse.ArgumentParser(description='Build a project as defined in recipes.json and ingredients.json.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    parser.add_argument('-c', '--clean', action='store_true', default=False, help='Clean the build folder. Removes all files (such as object and dependency files) EXCEPT for each of the build targets.')
    parser.add_argument('-p', '--purify', action='store_true', default=False, help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    parser.add_argument('-z', '--zip', action='store_true', default=False, help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    # TODO: Add ability to build just one target. Other flags/args?
    #   - Option to change default names for recipes.json and ingredients.json
    #   - Easier way to implement -c/-p than with boolean flag and if statement?
    # TODO: Change meaning of building, cleaning, purifying, and zipping if a target is specified
    # TODO: Add description of JSON files in help string. Link to github.
    
def get_command_line_args():
    return parser.parse_args()