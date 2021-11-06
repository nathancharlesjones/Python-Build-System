#! /bin/python3

import target

libtest_build_dir = "alt"
libtest = target.library(name="libtest",c_compiler="gcc",archiver="ar",archiver_flags=['rcs'],
	build_dir=libtest_build_dir,target='libtest.a',source_files=["lib/test/src/test_func.c"],
	include_dirs=["lib/test/inc"],pre_build_cmds=["echo Beginning build for libtest"],
	post_build_cmds=["echo Finished building libtest"])
print(libtest)

hello_world = target.executable(name='hello-world',c_compiler='gcc',linker='gcc',
	build_dir='build',target='main.exe',source_files=['src/main.c'],include_dirs=["lib/test/inc"],
	libraries=["test"],library_dirs=[libtest_build_dir],local_dependencies=[libtest],
	pre_build_cmds=["echo Beginning build for hello-world"],
	post_build_cmds=["echo Finished building hello-world","./build/main.exe"])
print(hello_world)

hello_world.build(True)

import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

for library in hello_world.libraries:
	print(find('lib{0}.a'.format(library), './'))
