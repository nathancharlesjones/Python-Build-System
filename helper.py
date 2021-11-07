import argparse
import subprocess
import os
import fnmatch

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing: " + cmd)
    process = subprocess.run([cmd], shell=True, text=True)
    if verbose and process.stdout:
        print("Output: " + process.stdout)

def file_exists(file):
    return os.path.exists(file)

def file_does_not_exist(file):
    return not file_exists(file)

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_command_line_args():
    parser = argparse.ArgumentParser(description="Python-based build system for C/C++ projects. Implemented like 'make' with an interface closer to 'cmake'. Builds projects that are defined in project_targets.py.")
    parser.add_argument('-t', '--target', action='store', dest='target', default='all', help='Specify a single target to be built, cleaned, purified, or zipped. All targets are built if none is specified.')
    non_build_option_group = parser.add_mutually_exclusive_group(required=True)
    non_build_option_group.add_argument('-b', '--build', action='store_const', const='build', dest='execute', help='Build the specified target (or all targets if no target was specified).')
    non_build_option_group.add_argument('-c', '--clean', action='store_const', const='clean', dest='execute', help='Clean the build folder for the specified target (or for all targets if no target was specified). Removes all files (such as object and dependency files) EXCEPT for each of the build targets and any zipped folders.')
    non_build_option_group.add_argument('-p', '--purify', action='store_const', const='purify', dest='execute', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    non_build_option_group.add_argument('-z', '--zip', action='store_const', const='zip', dest='execute', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    non_build_option_group.add_argument('-l', '--list', action='store_const', const='list', dest='execute', help="List the available target names, as defined in 'project_targets.py'. When used with verbose option, list all settings for all available targets.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    return parser.parse_args()

def get_dependencies_list(dep_file):
    dep_list = []
    if file_exists(dep_file):
        with open(dep_file) as f:
            deps = f.read()
        deps = deps.replace('\n',' ')
        dep_list_dirty = deps.split(' ')
        for item in dep_list_dirty:
            if file_exists(item):
                dep_list += [item]
    return dep_list

'''
Saving for posterity's sake, since the juxtaposition with my second solution, above, is interesting
to me.
1) The solution above is shorter, cleaner, and, I think, more robust. Why? I think because it has fewer requirements, fewer ways it could break. The code below requires each line of text to end in either a continuation character (backslash) or a complete file; it requires that each line have the character sequence ": " after which needs to come a space-separated list of files.
2) The code below actually has an error! Using the .remove method inside a for loop where I'm iterating over the same list that I've removing elements from is always an error, since iteration skips subsequent elements after I remove an item! Put differently, if I remove the item at position 2 the rest of the loop shifts to the left; the item at position 3 becomes the new item at position 2, the item at position 4 moves to position 3, etc. However, the loop still tries to access the item at position 3 on the next iteration of the loop, which means that it skips over whatever item was previously sitting at position 3 (and is now sitting in position 2)!
def get_dependencies_list(dep_file):
    dep_list = []
    if os.path.exists(dep_file):
        with open(dep_file) as deps:
            line = deps.readline()
            while line:
                if len(line) > 1:
                    while line[-2] == "\\":
                        line = line[:-2] + deps.readline()
                    colon_idx = line.find(': ')
                    if colon_idx != -1:
                        dep_list += line[colon_idx+2:line.find("\n")].split(' ')
                line = deps.readline()
    for item in dep_list:
        if item == '' or ' ' in item:
            dep_list.remove(item)
    return dep_list
'''

def remove_from_dict_all_except(dict, key):
    dict = { key : dict[key] }

def target_was_specified(args):
    return args.target != 'all'

def valid_target_name(targets, target):
    return target in targets