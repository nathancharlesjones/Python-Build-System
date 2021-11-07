import argparse
import subprocess
import os, fnmatch

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing: " + cmd)
    process = subprocess.run([cmd], shell=True, text=True)
    if verbose and process.stdout:
        print("Output: " + process.stdout)

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

def remove_from_dict_all_except(dict, key):
    dict = { key : dict[key] }

def target_was_specified(args):
    return args.target != 'all'

def valid_target_name(targets, target):
    return target in targets
