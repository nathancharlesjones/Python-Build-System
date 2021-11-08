# Python Build System

## What is it?

A Python script that reads a description of a C/C++ project from `project_targets.py` (see example below) and calls the specified compiler/assembler/linker/archiver to fully build the project. Python Build System automatically tracks file dependencies so it will only rebuild the parts of the project that are out of date with the files they depend on, like any modern build system. It's basically a simple version of GNU `make` written in Python, and which features a slightly easier way to define projects.

It accepts a number of command-line arguments that allow for:

- building an entire project,
- cleaning/purifying the build folder,
- zipping the project, or
- doing any of the above for a single target or all of the targets defined in `project_targets.py`.

It also comes with a Dockerfile I've been using to experiment with cross-platform development.

Example `project_targets.py`:

```
import target

def get_project_targets():
    targets = {}

    libtest_build_dir = "build-Simple-Build-System"
    libtest = target.library(
        name                =   "libtest",
        c_compiler          =   "gcc",
        archiver            =   "ar",
        archiver_flags      =   ['rcs'],
        build_dir           =   libtest_build_dir,
        target              =   'libtest.a',
        source_files        =   ["lib/test/src/test_func.c"],
        include_dirs        =   ["lib/test/inc"],
        pre_build_cmds      =   ["echo Beginning build for libtest"],
        post_build_cmds     =   ["echo Finished building libtest"]
    )

    targets[libtest.name] = libtest

    hello_world = target.executable(
        name                =   'hello_world',
        c_compiler          =   'gcc',
        c_flags             =   ['-g3','-O0'],
        linker              =   'gcc',
        build_dir           =   'build-Simple-Build-System',
        target              =   'main.exe',
        source_files        =   ['src/main.c'],
        include_dirs        =   ["lib/test/inc"],
        libraries           =   ["test", "m"],
        library_dirs        =   [libtest_build_dir],
        local_dependencies  =   [libtest],
        pre_build_cmds      =   ["echo Beginning build for hello-world"],
        post_build_cmds     =   ["echo Finished building hello-world",
                                 "./build-Simple-Build-System/main.exe"]
    )

    targets[hello_world.name] = hello_world

    return targets
```

## How do I use it?

Check out [this sample project](https://github.com/nathancharlesjones/Python-Build-System-Example) or follow the directions below:

1) Clone this repo into your desired project folder. I.e.
```
. <-- Root project folder
├── Python-Build-System
│   ├── Dockerfile
│   ├── README.md
│   ├── helper.py
│   ├── make.py
│   ├── example_project_targets.py
│   └── target.py
├── inc
├── src
└── Other project folders...
```
2) Create or edit `project_targets.py` to be of the following format:
```
import target

def get_project_targets():
    targets = {}

    # Define a new target, e.g. "new_library = target.library(...) or main = target.executable(...)"

    # Add the target to the dictionary of targets: targets[main.name] = main

    return targets
```
3) The Python module `target.py` defines two types of targets: `library` and `executable`. A `library` target builds a static library and `executable` builds an executable binary. They accept the parameters below. Not all are required; `make.py` should warn you when something is missing that's required.

#### `library` objects

| Field              | Type            | Required?                                          | Description                                                                                                                                                                                                                                                   |
|--------------------|-----------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | String          | No                                                 | Name to be used for this target. Used with `-t` when building/cleaning/purifying/zipping a single target.                                                                                                                                                     |
| build_dir          | String          | Yes                                                | Name of the directory in the project folder where build results should be placed. Doesn't need to be made ahead of time, as the program will create it if it does not exist.                                                                                         |
| target             | String          | Yes                                                | Name (and extension, if used) of the final library to be built (e.g. "libtest.a").                                                                                                                                                            |
| c_compiler         | String          | Yes, if `source_files` includes ".c" files         | Program to be used for compiling ".c" files. Can be the same as cpp_compiler if that is desired. Should match the exact program invocation used in a shell (e.g. "gcc", not "GCC").                                                                           |
| c_flags            | List of strings | No                                                 | List of flags to be passed to the C compiler.                                                                                                                                                                                                                 |
| cpp_compiler       | String          | Yes, if `source_files` includes ".cpp" files       | Program to be used for compiling ".cpp" files. Should match the exact program invocation used in a shell (e.g. "g++", not "G++").                                                                                                                             |
| cpp_flags          | List of strings | No                                                 | List of flags to be passed to the C++ compiler.                                                                                                                                                                                                               |
| assembler          | String          | Yes, if `source_files` includes ".s" or ".S" files | Program to be used for assembling ".s" and ".S" files. Can be the same as c_compiler or cpp_compiler if that is desired. Should match the exact program invocation used in the shell (e.g. "as", not "AS").                                                                                                                    |
| as_flags           | List of strings | No                                                 | List of flags to be passed to the assembler.                                                                                                                                                                                                                  |
| defines            | List of strings | No                                                 | List of defines to be passed to the compiler/assembler. Should not be prefixed with "-D", as this will get added by the program.                                                                                                                                   |
| include_dirs       | List of strings | No                                                 | List of include directories to be added to the compiler, relative to the project's root folder. Should not be prefixed with "-I ", as this will get added by the program.                                                                                     |
| source_files       | List of strings | Yes                                                | List of all source files to be used in the project; it's okay if the list is a mix of ".c", ".cpp", and ".s"/".S" files. Each entry should include a filepath relative to the project's root folder, i.e. "src/main.c".                                       |
| archiver           | String          | Yes                                                | Program to be used for final building of the static library. Should match exactly the program invocation used in the shell (e.g. "ar", not "AR").                                                                                                             |
| archiver_flags     | List of strings | No                                                 | List of flags to be passed to the archiver.                                                                                                                                                       |
| libraries          | List of strings | No                                                 | List of libraries to link against the final executable, including any locally built libraries. Should not be prefixed with "-l", as this will get added by the program.                                                                                       |
| library_dirs       | List of strings | No                                                 | List of directories in which to search for the required libraries, relative to the project's root folder (system folders need not be included).                                                                                                               |
| local_dependencies | List of strings | No                                                 | List of `target.library` objects that this program is dependent on. These need to be the actual `target.library` objects as each objects' build method will be invoked by the program when this executable is being built, to ensure that all files are up to date. |
| pre_build_cmds     | List of strings | No                                                 | List of shell commands to be executed prior to building this project. Should be typed exactly as they would be in the shell, e.g. "echo Building main".                                                                                                       |
| post_build_cmds    | List of strings | No                                                 | List of shell commands to be executed after building this project. Should be typed exactly as they would be in the shell, e.g. "./build/main".                                                                                                                |

#### `executable` objects

| Field              | Type            | Required?                                          | Description                                                                                                                                                                                                                                                   |
|--------------------|-----------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | String          | No                                                 | Name to be used for this target. Given to "-t" when building/cleaning/purifying/zipping a single target.                                                                                                                                                      |
| build_dir          | String          | Yes                                                | Name of the directory in the project folder where build results should be placed. Doesn't need to be made ahead of time, as the program will create it if it does not exist.                                                                                         |
| target             | String          | Yes                                                | Name (and extension, if used) of the final executable to be build (e.g. "main.exe", "myProg.elf").                                                                                                                                                            |
| c_compiler         | String          | Yes, if `source_files` includes ".c" files         | Program to be used for compiling ".c" files. Can be the same as cpp_compiler if that is desired. Should match the exact program invocation used in a shell (e.g. "gcc", not "GCC").                                                                           |
| c_flags            | List of strings | No                                                 | List of flags to be passed to the C compiler.                                                                                                                                                                                                                 |
| cpp_compiler       | String          | Yes, if `source_files` includes ".cpp" files       | Program to be used for compiling ".cpp" files. Should match the exact program invocation used in a shell (e.g. "g++", not "G++").                                                                                                                             |
| cpp_flags          | List of strings | No                                                 | List of flags to be passed to the C++ compiler.                                                                                                                                                                                                               |
| assembler          | String          | Yes, if `source_files` includes ".s" or ".S" files | Program to be used for assembling ".s" and ".S" files. Can be the same as c_compiler or cpp_compiler if that is desired. Should match the exact program invocation used in the shell (e.g. "as", not "AS").                                                                                                                     |
| as_flags           | List of strings | No                                                 | List of flags to be passed to the assembler.                                                                                                                                                                                                                  |
| defines            | List of strings | No                                                 | List of defines to be passed to the compiler/assembler. Should not be prefixed "-D", as this will get added by the program.                                                                                                                                   |
| include_dirs       | List of strings | No                                                 | List of include directories to be added to the compiler, relative to the project's root folder. Should not be prefixed with "-I ", as this will get added by the program.                                                                                     |
| source_files       | List of strings | Yes                                                | List of all source files to be used in the project; it's okay if the list is a mix of ".c", ".cpp", and ".s"/".S" files. Each entry should include a filepath relative to the project's root folder, i.e. "src/main.c".                                       |
| linker             | String          | Yes                                                | Program to be used for final linking of an executable. Should match exactly the program invocation used in the shell (e.g. "ld" or "gcc", not "GCC").                                                                                                         |
| linker_flags       | List of strings | No                                                 | List of flags to be passed to the linker.                                                                                                                                                                                                                     |
| linker_script      | String          | No                                                 | Linker script to be given to the linker (for embedded systems). Should not be prefixed by "-T", as this will get added by the program.                                                                                                                        |
| libraries          | List of strings | No                                                 | List of libraries to link against the final executable, including any locally built libraries. Should not be prefixed with "-l", as this will get added by the program.                                                                                       |
| library_dirs       | List of strings | No                                                 | List of directories in which to search for the required libraries, relative to the project's root folder (system folders need not be included).                                                                                                               |
| local_dependencies | List of strings | No                                                 | List of `target.library` objects that this program is dependent on. These need to be the actual `target.library` objects as each objects' build method will be invoked by the program when this executable is being built, to ensure that all files are up to date. |
| pre_build_cmds     | List of strings | No                                                 | List of shell commands to be executed prior to building this project. Should be typed exactly as they would be in the shell, e.g. "echo Building main".                                                                                                       |
| post_build_cmds    | List of strings | No                                                 | List of shell commands to be executed after building this project. Should be typed exactly as they would be in the shell, e.g. "./build/main".                                                                                                                |

4) If you're planning on using the Dockerfile:
    - Inspect the Dockerfile to see if there are any additional programs you'll want. Only `build-essentials` is required for normal GCC projects (it includes `gcc`, `g++`, and `make`).
    - Download and install [Docker](https://docs.docker.com/get-docker/). Ensure it is running.
    - From a shell on your system, navigate to this folder (`Python-Build-System`) and run the following, where `<NAME>` is the name you want to give your Docker image:

    `docker build -f Dockerfile -t <NAME> .`
    
    - Wait. Building this Docker image takes a good 5-10 minutes on my system.
5) From a shell on your system, navigate now to your project's root folder. Run the following to build your project:

`./Python-Build-System/make.py -b`

Or, if you're using Docker:

`docker run -it --rm -v ${PWD}:/app devenv-simple-build-system /bin/bash -c "./Python-Build-System/make.py -b"`

If you see an error like `bash: ./Simple-Build-System/make.py: /bin/python3^M: bad interpreter: No such file or directory` it's probably because you're editing `make.py` on Windows (and using Windows line endings, CRLF) but the file is being run on a Unix machine (which is expecting Unix line endings, LF only). If this is the problem, you'll need to figure out how to change to Unix line endings. The simplest fix seems to be to change the default line ending in your text editor; I use Sublime Text and [this thread](https://stackoverflow.com/questions/39680585/how-do-configure-sublime-to-always-convert-to-unix-line-endings-on-save) recommended I add the following keys to my user settings:
```
// Determines what character(s) are used to terminate each line in new files.
// Valid values are 'system' (whatever the OS uses), 'windows' (CRLF) and
// 'unix' (LF only).
"default_line_ending": "unix",
// Display file encoding in the status bar
"show_encoding": true,
// Display line endings in the status bar
"show_line_endings": true
```
Once I did, I could select the line ending I wanted on the bottom toolbar in Sublime Text. Many forums I read when trying to solve this problem also recommended a program called dos2unix.

6) The file `make.py` defines the command-line interface for building the project. Run it with the `-h` flag instead of the `-b` flag to see the following help information:
```
usage: make.py [-h] [-t TARGET] (-b | -c | -p | -z | -l) [-v]

Python-based build system for C/C++ projects. Implemented like 'make' with an interface closer to 'cmake'. Builds projects that are defined in project_targets.py.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Specify a single target to be built, cleaned, purified, or zipped. All targets are built if none is specified.
  -b, --build           Build the specified target (or all targets if no target was specified).
  -c, --clean           Clean the build folder for the specified target (or for all targets if no target
                        was specified). Removes all files (such as object and dependency files) EXCEPT for
                        each of the build targets and any zipped folders.
  -p, --purify          Purify the build folder. Removes the build folder and all subfiles and 
                        subdirectories for each target.
  -z, --zip             Purify the build folder. Removes the build folder and all subfiles and 
                        subdirectories for each target.
  -l, --list            List the available target names, as defined in 'project_targets.py'. When used 
                        with verbose option, list all settings for all available targets.
  -v, --verbose         Verbose output. Show the recipe configuration prior to it being built and show 
                        all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)
```
7) Later on, feel free to edit or extend `make.py`! It's just a Python script, after all.

## Why'd you do it?

Apparently because I'm a glutton for punishment.

In all seriousness, I was learning how to use CMake at the time and as much as I liked how easy it was to define and build a simple project, I felt like overall it was a complicated program that I might not be able to fully understand. And when I can't understand something, there inevitably seems to come a day when I'm forced to build my project in a specific way "because it works when I do it that way and it doesn't if I don't".

At the same time, I was struck by the idea that entire projects can be built with something like three simple shell commands, of the format:
1) For compiling object files: `COMPILER   COMPILER_FLAGS   DEFINES   INCLUDES   DEPENDENCY FLAGS   -c   SOURCE_FILE   -o   OBJECT_FILE`
2) For building static libraries: `ARCHIVER   ARCHIVER_FLAGS   DEFINES   LIBRARY_FILE   OBJECT_FILES`
3) For building executables: `LINKER   LINKER_FLAGS   LINKER_SCRIPT   DEFINES   INCLUDES   OBJECT_FILES   LIBRARY_DIRS   LIBRARIES   -o   EXECUTABLE`

I thought, "Couldn't someone write a program that just listed these parameters and ran the right command for each listed file with the proper arguments in order to build an entire project?" I thought the whole thing might only be a few dozen lines of Python.

And I think maybe you _could_ do it that succinctly, but my final script ended up being quite a bit longer in order to support:
- Command-line arguments and their execution
- Checking of input values (so a program with ".cpp" files has a C++ compiler listed, for instance)
- Generating and checking dependencies so parts of a project aren't rebuilt if their dependencies haven't changed
- Working with files and filepaths in the form of strings

Ultimately I'm happy with the outcome. It feels much easier to use (and much easier to later extend!) than `make` while keeping the build folder uncluttered. Enjoy!
