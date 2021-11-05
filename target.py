from subprocess_helper import execute_shell_cmd
import os

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
        for file in self.object_files:
            if not os.path.exists(file) or not os.path.exists('{0}/{1}'.format(self.build_dir,self.target)) or os.path.getmtime(file) > os.path.getmtime('{0}/{1}'.format(self.build_dir,self.target)):
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
            
            if ".c" in this_source_file:
                compiler = self.c_compiler
                compiler_flags = self.c_flags
                this_object_file = this_source_file.replace(".c",".o")
            else:
                compiler = self.cpp_compiler
                compiler_flags = self.cpp_flags
                this_object_file = this_source_file.replace(".cpp",".o")
                this_object_file = this_source_file.replace(".cxx",".o")
            
            if not os.path.exists("{0}/{1}".format(self.build_dir,this_object_file)) or os.path.getmtime(this_source_file) > os.path.getmtime("{0}/{1}".format(self.build_dir,this_object_file)):
                compiler_flags_str = ' '.join(compiler_flags)
                defines_str = ' '.join(self.defines)
                include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in self.include_dirs])
                compile_obj_file_cmd = "{0} {1} {2} {3} -c {4} -o {5}/{6}".format(compiler,compiler_flags_str,defines_str,include_dirs_str,this_source_file,self.build_dir,this_object_file)
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
        pass

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


    def __str__(self):
        return "Test"



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
        
        self.pre_build_cmds = pre_build_cmds
        
        self.post_build_cmds = post_build_cmds

    def form_build_cmd(self, verbose=False):
        archiver_flags_str = ' '.join(self.archiver_flags)
        defines_str = ' '.join(self.defines)
        object_files_str = ' '.join(self.object_files)
        return "{0} {1} {2} {3}/{4} {5}".format(self.archiver,archiver_flags_str,defines_str,self.build_dir,self.target,object_files_str)

    def __str__(self):
        return "test"
