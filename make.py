import json
import sys
import subprocess
import argparse

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing: " + cmd)
    process = subprocess.run([cmd], shell=True, text=True)
    if verbose and process.stdout:
        print("Output: " + process.stdout)

def main():
    parser = argparse.ArgumentParser(description='Build a project as defined in recipes.json and ingredients.json.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    args = parser.parse_args()
    
    #import os
    #print(os.getcwd())

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
        if args.verbose:
            print(json.dumps(this_recipe, indent=4))

        #this_name = this_recipe['name']
        #this_compiler = this_recipe['compiler']
        #this_linker = this_recipe['linker']
        #this_build_dir = this_recipe['build_dir']
        #this_target = this_recipe['target']
        #this_target_type = this_recipe['target_type']
        #these_compiler_flags = this_recipe['compiler_flags']
        #these_defines = this_recipe['defines']
        #these_source_files = this_recipe['source_files']
        these_object_files = []
        for this_source_file in this_recipe['source_files']:
            these_object_files.append(this_recipe['build_dir'] + "/" + this_source_file.replace(".c", ".o"))
        #these_include_dirs = this_recipe['include_dirs']
        #these_libraries = this_recipe['libraries']
        #these_library_dirs = this_recipe['library_dirs']
        #these_linker_flags = this_recipe['linker_flags']
        #these_pre_build_commands = this_recipe['pre_build_commands']
        #these_post_build_commands = this_recipe['post_build_commands']

        for cmd in this_recipe['pre_build_commands']:
            execute_shell_cmd(cmd, args.verbose)

        for this_source_file in this_recipe['source_files']:
            if 'compiler' not in this_recipe:
                print("**ERROR**: Compiler not defined for " + this_recipe['name'] + ". Aborting.")
                sys.exit()
            cmd = ' '.join([this_recipe['compiler'],
                this_recipe['compiler_flags'],
                this_recipe['defines'],
                '-I '+'-I '.join(this_recipe['include_dirs']),
                "-c",
                this_source_file,
                "-o",
                this_recipe['build_dir']+ "/" + this_source_file.replace(".c", ".o") ])
            execute_shell_cmd(cmd, args.verbose)

        if this_recipe['target_type'] == 'executable':
            if 'linker' not in this_recipe:
                print("**ERROR**: Linker not defined for " + this_recipe['name'] + ". Skipping linking step.")
                continue
            cmd = ' '.join([this_recipe['linker'],
                    this_recipe['compiler_flags'],
                    this_recipe['defines'],
                    '-I '+'-I '.join(this_recipe['include_dirs']),
                    ' '.join(these_object_files),
                    "-o",
                    this_recipe['build_dir']+ "/" + this_recipe['target'] ])
        elif this_recipe['target_type'] == 'library':
            if 'archiver' not in this_recipe:
                print("**ERROR**: Archiver not defined for " + this_recipe['name'] + ". Skipping archiving step.")
                continue
            cmd = ' '.join([this_recipe['archiver'],
                    this_recipe['archiver_flags'],
                    this_recipe['defines'],
                    this_recipe['build_dir']+ "/" + this_recipe['target'],
                    ' '.join(these_object_files) ])
        else:
            print("**ERROR**: Invalid target type for " + this_recipe['name'])
            print("Continuing with next target")
            continue

        execute_shell_cmd(cmd, args.verbose)
        
        for cmd in this_recipe['post_build_commands']:
            execute_shell_cmd(cmd, args.verbose)

if __name__ == "__main__":
    main()
