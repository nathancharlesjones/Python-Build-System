# Simple Build System

## Building
- Install Docker and ensure it is running
- Edit "Dockerfile" to include any programs (or dependencies?) you need to build your project
- Run "docker build -f Dockerfile -t devenv-simple-build-system ." from Simple-Build-System folder to build the Docker image
- Copy dependencies the first time the container is run (to put them in the right place on the host machine)
- Run "docker run -it --rm -v ${PWD}:/app devenv-simple-build-system /bin/bash -c "make.py" from Simple-Build-System folder
	- If you see an error like "bash: ./Simple-Build-System/make.py: /bin/python3^M: bad interpreter: No such file or directory" it's probably because you're editing make.py on Windows (and using Windows line endings, CRLF) but the file is being run on a Unix machine (which is expecting Unix line endings, LF only). If this is the problem, you'll need to figure out how to change to Unix line endings. The simplest fix seems to be to change the default line ending in your text editor; I use Sublime Text and this thread (https://stackoverflow.com/questions/39680585/how-do-configure-sublime-to-always-convert-to-unix-line-endings-on-save) recommended I add the following keys to my user settings:
	// Determines what character(s) are used to terminate each line in new files.
    // Valid values are 'system' (whatever the OS uses), 'windows' (CRLF) and
    // 'unix' (LF only).
    "default_line_ending": "unix",
    // Display file encoding in the status bar
    "show_encoding": true,
    // Display line endings in the status bar
    "show_line_endings": true
    Once I did, I could select the line ending I wanted on the bottom toolbar. Many forums I read when trying to solve this problem also recommended a program called dos2unix. 
	- Or "docker run -it --rm -v ${PWD}:/app devenv-simple-build-system /bin/bash -c "./Simple-Build-System/make.py"" from project root
	- "/app" should match the "WORKDIR" variable from the Dockerfile
	- Alias?
- Run just "docker run -it --rm -v ${PWD}:/app devenv-simple-build-system /bin/bash" to get to a shell