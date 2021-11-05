#! /bin/python3

import json
import sys
import subprocess
import argparse
import os

# TODO: Add more comments
# TODO: How to add subprojects and other dependencies?

list_of_valid_target_types = [ 'executable', 'library' ]

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing: " + cmd)
    process = subprocess.run([cmd], shell=True, text=True)
    if verbose and process.stdout:
        print("Output: " + process.stdout)

def main():
    parser = argparse.ArgumentParser(description='Build a project as defined in recipes.json and ingredients.json.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    parser.add_argument('-c', '--clean', action='store_true', default=False, help='Clean the build folder. Removes all files (such as object and dependency files) EXCEPT for each of the build targets.')
    parser.add_argument('-p', '--purify', action='store_true', default=False, help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    parser.add_argument('-z', '--zip', action='store_true', default=False, help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    args = parser.parse_args()
    # TODO: Add ability to build just one target. Other flags/args?
    #   - Option to change default names for recipes.json and ingredients.json
    #   - Easier way to implement -c/-p than with boolean flag and if statement?
    # TODO: Change meaning of building, cleaning, purifying, and zipping if a target is specified
    # TODO: Add description of JSON files in help string. Link to github.
    
    # TODO: Add importing ingredients.json and using that to populate each recipe
    # TODO: Refactor so that the code below reads better
    # TODO: Add zip commands
    # TODO: Add dependency ... stuff
    # TODO: Add checks to only build if dependency is newer than target

    try:
        recipes_file = open('recipes.json','r')
    except IOError:
        print("**ERROR**: Could not find '../recipes.json'. Ensure that this file is present in the project root.")
        sys.exit()

    try:
        recipes = json.load(recipes_file)
    except json.decoder.JSONDecodeError:
        print("**ERROR**: Could not read 'recipes.json'. Ensure that this file has proper JSON syntax and follows the project conventions for defining recipe values. See here for more information.")
        sys.exit()

    for this_recipe in recipes["all_recipes"]:
        
        # Set safe values for name
        name = this_recipe['name'] if 'name' in this_recipe else 'unnamed recipe'

        # Check for required keys; abort if not present
        compiler = this_recipe['compiler'] if 'compiler' in this_recipe else str(print("**ERROR**: Compiler not defined for " + name + ". Aborting.")) and sys.exit()
        target_type = this_recipe['target_type'] if ('target_type' in this_recipe and this_recipe['target_type'] in list_of_valid_target_types) else str(print("**ERROR**: Invalid target type for " + name + ". Aborting.")) and sys.exit()
        if target_type == 'executable':
            if 'linker' in this_recipe:
                linker = this_recipe['linker']
            else:
                print("**ERROR**: Linker not defined for " + name + ". Aborting.")
                sys.exit()
        elif target_type == 'library':
            if 'archiver' in this_recipe:
                archiver = this_recipe['archiver']
            else:
                print("**ERROR**: Archiver not defined for " + name + ". Aborting.")
                sys.exit()
        build_dir = this_recipe['build_dir'] if 'build_dir' in this_recipe else str(print("**ERROR**: Build directory not specified for " + name + ". Aborting.")) and sys.exit()
        target = this_recipe['target'] if 'target' in this_recipe else str(print("**ERROR**: Target value not defined for " + name + ". Aborting.")) and sys.exit()
        source_files = this_recipe['source_files'] if ('source_files' in this_recipe and len(this_recipe['source_files']) != 0) else str(print("**ERROR**: Source files not defined for " + name + ". Aborting.")) and sys.exit()

        if args.clean:
            execute_shell_cmd("find "+build_dir+r" -mindepth 1 -maxdepth 1 -type d -exec rm -r {} \;", args.verbose)
            continue

        if args.purify:
            execute_shell_cmd("rm -r -f "+build_dir, args.verbose)
            continue

        these_object_files = []
        for this_source_file in this_recipe['source_files']:
            these_object_files.append(this_recipe['build_dir'] + "/" + this_source_file.replace(".c", ".o"))

        # Check for optional keys
        compiler_flags = this_recipe['compiler_flags'] if 'compiler_flags' in this_recipe else ""
        include_dirs = this_recipe['include_dirs'] if 'include_dirs' in this_recipe else ""
        libraries = this_recipe['libraries'] if 'libraries' in this_recipe else ""
        library_dirs = this_recipe['library_dirs'] if 'library_dirs' in this_recipe else ""
        archiver_flags = this_recipe['archiver_flags'] if 'archiver_flags' in this_recipe else ""
        linker_flags = this_recipe['linker_flags'] if 'linker_flags' in this_recipe else ""
        defines = this_recipe['defines'] if 'defines' in this_recipe else ""
        pre_build_commands = this_recipe['pre_build_commands'] if 'pre_build_commands' in this_recipe else ""
        post_build_commands = this_recipe['post_build_commands'] if 'post_build_commands' in this_recipe else ""

        if args.verbose:
            print("Building the following recipe:")
            print(json.dumps(this_recipe, indent=4))

        for pre_build_cmd in pre_build_commands:
            execute_shell_cmd(pre_build_cmd, args.verbose)

        for this_source_file in source_files:
            path, filename = os.path.split(this_source_file)
            execute_shell_cmd("mkdir -p "+build_dir+"/"+path, args.verbose)
            compile_obj_file_cmd = ' '.join([compiler,compiler_flags,defines,'-I '+'-I '.join(include_dirs),"-c",this_source_file,"-o",build_dir+"/"+this_source_file.replace(".c", ".o")])
            execute_shell_cmd(compile_obj_file_cmd, args.verbose)

        # TODO: Add a way for libraries to be searched for in the recipe list
        #   - Separate into libraries.json and executables.json?

        if this_recipe['target_type'] == 'executable':
            build_cmd = ' '.join([linker,linker_flags,defines,'-I '+'-I '.join(include_dirs),' '.join(these_object_files),'-L '+'-L '.join(library_dirs),'-l'+'-l'.join(libraries),"-o",build_dir+"/"+target])
        elif this_recipe['target_type'] == 'library':
            build_cmd = ' '.join([archiver, archiver_flags, defines, build_dir+"/"+target,' '.join(these_object_files)])
        else:
            print("**ERROR**: Invalid target type for " + name)
            print("Continuing with next target")
            continue

        execute_shell_cmd(build_cmd, args.verbose)
        
        for post_build_cmd in post_build_commands:
            execute_shell_cmd(post_build_cmd, args.verbose)

if __name__ == "__main__":
    main()
