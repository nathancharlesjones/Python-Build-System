from subprocess_helper import execute_shell_cmd

class target:
    """ Interface class for defining project targets. """

    def __init__(self):
        """ Helpful docstring """
        pass

    def build(self, verbose=False):
        pass

    def compile_object_files(self, verbose=False):
        import os
        for this_source_file in self.source_files:
            path, filename = os.path.split(this_source_file)
            execute_shell_cmd("mkdir -p {0}/{1}".format(self.build_dir, path), args.verbose)
            compile_obj_file_cmd = "{0} {1} {2} {3} -c {4} -o {5}/{6}".format(self.compiler,self.compiler_flags,self.defines,' '.join(["-I "+inc_dir for inc_dir in self.include_dirs]),"-c",this_source_file,"-o",self.build_dir,this_source_file.replace(".c", ".o"))
            execute_shell_cmd(compile_obj_file_cmd, args.verbose)

    def build_local_dependencies(self, verbose=False):
        for this_target in self.local_dependencies:
            this_target.build()

    def clean(self, verbose=False):
        execute_shell_cmd("find {0}".format(self.build_dir)+r" -mindepth 1 -maxdepth 1 -type d -exec rm -r {} \;", args.verbose)

    def purify(self, verbose=False):
        execute_shell_cmd("rm -r -f {0}".format(self.build_dir), args.verbose)

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
        

    def build(self, verbose=False):
        pass


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

    def build(self, verbose=False):
        pass

    def __str__(self):
        return "test"
