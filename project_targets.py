import target

# TODO: Add default rules/ingredients
# TODO: Make these variables instead of a function?

def get_project_targets():
	targets = {}

	libtest_build_dir = "build"
	libtest = target.library(name="libtest",c_compiler="gcc",archiver="ar",archiver_flags=['rcs'],
		build_dir=libtest_build_dir,target='libtest.a',source_files=["lib/test/src/test_func.c"],
		include_dirs=["lib/test/inc"],pre_build_cmds=["echo Beginning build for libtest"],
		post_build_cmds=["echo Finished building libtest"])

	targets[libtest.name] = libtest

	hello_world = target.executable(name='hello_world',c_compiler='gcc',linker='gcc',
		build_dir='build',target='main.exe',source_files=['src/main.c'],include_dirs=["lib/test/inc"],
		libraries=["test", "m"],library_dirs=[libtest_build_dir],local_dependencies=[libtest],
		pre_build_cmds=["echo Beginning build for hello-world"],
		post_build_cmds=["echo Finished building hello-world","./build/main.exe"])

	targets[hello_world.name] = hello_world

	return targets