import argparse

parser = None

def initialize_command_line_interface():
    global parser
    parser = argparse.ArgumentParser(description='Build a project as defined in recipes.json and ingredients.json.')
    parser.add_argument('-t', '--target', action='store', dest='target', default='all', help='Specify a single target to be built, cleaned, purified, or zipped. All targets are built if none is specified.')
    non_build_option_group = parser.add_mutually_exclusive_group()
    non_build_option_group.add_argument('-c', '--clean', action='store_const', const='clean', dest='execute', default='build', help='Clean the build folder for the specified target (or for all targets if no target was specified). Removes all files (such as object and dependency files) EXCEPT for each of the build targets.')
    non_build_option_group.add_argument('-p', '--purify', action='store_const', const='purify', dest='execute', default='build', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    non_build_option_group.add_argument('-z', '--zip', action='store_const', const='zip', dest='execute', default='build', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    
def get_command_line_args():
    return parser.parse_args()