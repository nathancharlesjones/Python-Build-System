from helper import execute_shell_cmd, find, get_dependencies_list
import os

# TODO: Add more comments

class target:
    """ Parent class for defining project targets. """

    def __init__(self):
        raise NameError("Class target does not support creating objects; use target.executable or target.library instead.")

    def build(self, verbose=False):
        for pre_build_cmd in self.pre_build_cmds:
            execute_shell_cmd(pre_build_cmd, verbose)
        
        self.compile_object_files()
        self.build_local_dependencies()
        
        built=False
        for file in self.object_files+self.local_dep_target_list:
            # If the target doesn't exist OR object files or library files are newer than target...
            if not os.path.exists('{0}/{1}'.format(self.build_dir,self.target)) or os.path.getmtime(file) > os.path.getmtime('{0}/{1}'.format(self.build_dir,self.target)):
                build_cmd = self.form_build_cmd()
                execute_shell_cmd(build_cmd, verbose)
                built=True
                break
        if not built:
            print("Nothing to be done for {0}".format(self.name))
        
        for post_build_cmd in self.post_build_cmds:
            execute_shell_cmd(post_build_cmd, verbose)

    def compile_object_files(self, verbose=False):
        import os
        for this_source_file in self.source_files:
            path, filename = os.path.split(this_source_file)
            execute_shell_cmd("mkdir -p {0}/{1}".format(self.build_dir, path), verbose)
            
            if os.path.splitext(this_source_file)[1] == ".c":
                compiler = self.c_compiler
                compiler_flags = self.c_flags
                this_object_file = this_source_file.replace(".c",".o")
                this_dep_file = this_source_file.replace(".c",".d")
            elif os.path.splitext(this_source_file)[1] == ".cpp":
                compiler = self.cpp_compiler
                compiler_flags = self.cpp_flags
                this_object_file = this_source_file.replace(".cpp",".o")
                this_dep_file = this_source_file.replace(".cpp",".d")
            else:
                print("**WARNING**: Unknown file extension, {0}. Expecting '.c' or '.cpp'.".format(this_source_file))
            
            dep_list = get_dependencies_list("{0}/{1}".format(self.build_dir,this_dep_file))

            # if object file doesn't exist or object file dependencies are newer than object file...
            build = False
            if not os.path.exists("{0}/{1}".format(self.build_dir,this_object_file)):
                build = True
            for file in dep_list:
                if os.path.getmtime(file) > os.path.getmtime("{0}/{1}".format(self.build_dir,this_object_file)):
                    build = True

            if build:
                compiler_flags_str = ' '.join(compiler_flags)
                defines_str = ' '.join(self.defines)
                include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in self.include_dirs])
                compile_obj_file_cmd = "{0} {1} {2} {3} -MMD -MF {4}/{5} -c {6} -o {4}/{7}".format(compiler,compiler_flags_str,defines_str,include_dirs_str,self.build_dir,this_dep_file,this_source_file,this_object_file)
                print(compile_obj_file_cmd)
                execute_shell_cmd(compile_obj_file_cmd, verbose)
            else:
                print("Nothing to be done for {0}".format(this_object_file))

    def build_local_dependencies(self, verbose=False):
        for this_target in self.local_dependencies:
            this_target.build()

    def form_build_cmd(self, verbose=False):
        pass

    def clean(self, verbose=False):
        execute_shell_cmd("find {0}".format(self.build_dir)+r" -mindepth 1 -maxdepth 1 -type d -exec rm -r {} \;", verbose)

    def purify(self, verbose=False):
        execute_shell_cmd("rm -r -f {0}".format(self.build_dir), verbose)

    def zip(self, verbose=False):
        execute_shell_cmd("zip -r {0}/{1}.zip {0}/{2} {3}".format(self.build_dir,self.name,self.target,self.local_dep_target_list), verbose)

    def show(self, verbose=False):
        pass

    def execute(self, cmd, verbose=False):
        if cmd == 'clean':
            self.clean(verbose)
        elif cmd == 'purify':
            self.purify(verbose)
        elif cmd == 'zip':
            self.zip(verbose)
        elif cmd == 'list':
            self.show(verbose)
        elif cmd == 'build':
            self.build(verbose)

    def __str__(self):
        pass

class executable(target):
    """ Helpful docstring """

    def __init__(self,linker,build_dir,target,source_files,name='unnamed target',
        c_compiler='',c_flags=[],cpp_compiler='',cpp_flags=[],
        defines=[],linker_flags=[],include_dirs=[],libraries=[],
        library_dirs=[],local_dependencies=[],pre_build_cmds=[],post_build_cmds=[]):
        """ Helpful docstring """
        self.name = name

        self.source_files = source_files
        if len(self.source_files) == 0:
            raise ValueError("No source files listed for {0}".format(self.name))
        
        self.c_compiler = c_compiler
        for this_source_file in self.source_files:
            if ".c" in this_source_file and self.c_compiler == '':
                raise ValueError("No C compiler provided for {0}".format(self.name))
        
        self.c_flags = c_flags

        self.cpp_compiler = cpp_compiler
        for this_source_file in self.source_files:
            if ".cpp" in this_source_file or ".cxx" in this_source_file and self.cpp_compiler == '':
                raise ValueError("No C++ compiler provided for {0}".format(self.name))
        
        self.cpp_flags = cpp_flags
        
        self.defines = defines
        
        self.linker = linker
        
        self.linker_flags = linker_flags
        
        self.build_dir = build_dir
        
        self.target = target
        
        self.include_dirs = include_dirs
        
        self.object_files = []
        for this_source_file in self.source_files:
            self.object_files.append("{0}/{1}".format(self.build_dir,this_source_file.replace(".c", ".o")))
        
        self.libraries = libraries
        
        self.library_dirs = library_dirs
        
        self.local_dependencies = local_dependencies
        self.local_dep_target_list = ["{0}/{1}".format(dep.build_dir,dep.target) for dep in self.local_dependencies]
        
        self.pre_build_cmds = pre_build_cmds
        
        self.post_build_cmds = post_build_cmds
        

    def form_build_cmd(self, verbose=False):
        linker_flags_str = ' '.join(self.linker_flags)
        defines_str = ' '.join(self.defines)
        include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in self.include_dirs])
        object_files_str = ' '.join(self.object_files)
        library_dirs_str = ' '.join(["-L "+lib_dir for lib_dir in self.library_dirs])
        libraries_str = ' '.join(["-l"+lib for lib in self.libraries])
        return "{0} {1} {2} {3} {4} {5} {6} -o {7}/{8}".format(self.linker,linker_flags_str,defines_str,include_dirs_str,object_files_str,library_dirs_str,libraries_str,self.build_dir,self.target)


    def show(self, verbose=False):
        if not verbose:
            print("- {0}".format(self.name))
        else:
            print(self)


    def __str__(self):
        repr = '''{1} is defined as follows:
- {0}{1}
- {2}{3}
- {4}{5}
- {6}{7}
- {8}{9}
- {10}{11}
- {12}{13}
- {14}{15}
- {16}{17}
- {18}{19}
- {20}{21}
- {22}{23}
- {24}{25}
- {26}{27}
- {28}{29}
- {30}{31}
- {32}{33} '''.format( "name:".ljust(25,'.'),
                        self.name,
                        "target:".ljust(25,'.'),
                        self.target,
                        "build_dir:".ljust(25,'.'),
                        self.build_dir,
                        "c_compiler:".ljust(25,'.'),
                        self.c_compiler,
                        "c_flags:".ljust(25,'.'),
                        self.c_flags,
                        "cpp_compiler:".ljust(25,'.'),
                        self.cpp_compiler,
                        "cpp_flags:".ljust(25,'.'),
                        self.cpp_flags,
                        "linker:".ljust(25,'.'),
                        self.linker,
                        "linker_flags:".ljust(25,'.'),
                        self.linker_flags,
                        "defines:".ljust(25,'.'),
                        self.defines,
                        "include_dirs:".ljust(25,'.'),
                        self.include_dirs,
                        "source_files:".ljust(25,'.'),
                        self.source_files,
                        "libraries:".ljust(25,'.'),
                        self.libraries,
                        "library_dirs:".ljust(25,'.'),
                        self.library_dirs,
                        "local_dependencies:".ljust(25,'.'),
                        [dep.name for dep in self.local_dependencies],
                        "pre_build_cmds:".ljust(25,'.'),
                        self.pre_build_cmds,
                        "post_build_cmds:".ljust(25,'.'),
                        self.post_build_cmds)
        return repr



class library(target):
    """ Helpful docstring """

    def __init__(self,archiver,build_dir,target,source_files,name='unnamed target',
        c_compiler='',c_flags=[],cpp_compiler='',cpp_flags=[],
        defines=[],archiver_flags=[],include_dirs=[],libraries=[],
        library_dirs=[],local_dependencies=[],pre_build_cmds=[],post_build_cmds=[]):
        """ Helpful docstring """
        self.name = name

        self.source_files = source_files
        if len(self.source_files) == 0:
            raise ValueError("No source files listed for {0}".format(self.name))
        
        self.c_compiler = c_compiler
        for this_source_file in self.source_files:
            if ".c" in this_source_file and self.c_compiler == '':
                raise ValueError("No C compiler provided for {0}".format(self.name))
        
        self.c_flags = c_flags

        self.cpp_compiler = cpp_compiler
        for this_source_file in self.source_files:
            if ".cpp" in this_source_file or ".cxx" in this_source_file and self.cpp_compiler == '':
                raise ValueError("No C++ compiler provided for {0}".format(self.name))
        
        self.cpp_flags = cpp_flags
        
        self.defines = defines
        
        self.archiver = archiver
        
        self.archiver_flags = archiver_flags
        
        self.build_dir = build_dir
        
        self.target = target
        
        self.include_dirs = include_dirs
        
        self.object_files = []
        for this_source_file in self.source_files:
            self.object_files.append("{0}/{1}".format(self.build_dir,this_source_file.replace(".c", ".o")))
        
        self.libraries = libraries
        
        self.library_dirs = library_dirs
        
        self.local_dependencies = local_dependencies
        self.local_dep_target_list = ["{0}/{1}".format(dep.build_dir,dep.target) for dep in self.local_dependencies]
        
        self.pre_build_cmds = pre_build_cmds
        
        self.post_build_cmds = post_build_cmds

    def form_build_cmd(self, verbose=False):
        archiver_flags_str = ' '.join(self.archiver_flags)
        defines_str = ' '.join(self.defines)
        object_files_str = ' '.join(self.object_files)
        return "{0} {1} {2} {3}/{4} {5}".format(self.archiver,archiver_flags_str,defines_str,self.build_dir,self.target,object_files_str)

    def show(self, verbose=False):
        if not verbose:
            print("- {0}".format(self.name))
        else:
            print(self)

    def __str__(self):
        repr = '''{1} is defined as follows:
- {0}{1}
- {2}{3}
- {4}{5}
- {6}{7}
- {8}{9}
- {10}{11}
- {12}{13}
- {14}{15}
- {16}{17}
- {18}{19}
- {20}{21}
- {22}{23}
- {24}{25}
- {26}{27}
- {28}{29}
- {30}{31}
- {32}{33} '''.format( "name:".ljust(25,'.'),
                        self.name,
                        "target:".ljust(25,'.'),
                        self.target,
                        "build_dir:".ljust(25,'.'),
                        self.build_dir,
                        "c_compiler:".ljust(25,'.'),
                        self.c_compiler,
                        "c_flags:".ljust(25,'.'),
                        self.c_flags,
                        "cpp_compiler:".ljust(25,'.'),
                        self.cpp_compiler,
                        "cpp_flags:".ljust(25,'.'),
                        self.cpp_flags,
                        "archiver:".ljust(25,'.'),
                        self.archiver,
                        "archiver_flags:".ljust(25,'.'),
                        self.archiver_flags,
                        "defines:".ljust(25,'.'),
                        self.defines,
                        "include_dirs:".ljust(25,'.'),
                        self.include_dirs,
                        "source_files:".ljust(25,'.'),
                        self.source_files,
                        "libraries:".ljust(25,'.'),
                        self.libraries,
                        "library_dirs:".ljust(25,'.'),
                        self.library_dirs,
                        "local_dependencies:".ljust(25,'.'),
                        [dep.name for dep in self.local_dependencies],
                        "pre_build_cmds:".ljust(25,'.'),
                        self.pre_build_cmds,
                        "post_build_cmds:".ljust(25,'.'),
                        self.post_build_cmds)
        return repr
