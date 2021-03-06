Enhancements for standard library's cmd module.

Drop-in replacement adds several features for command-prompt tools:

    * Searchable command history (commands: "hi", "li", "run")
    * Load commands from file, save to file, edit commands in file
    * Multi-line commands
    * Case-insensitive commands
    * Special-character shortcut commands (beyond cmd's "@" and "!")
    * Settable environment parameters
    * Parsing commands with flags
    * > (filename), >> (filename) redirect output to file
    * < (filename) gets input from file
    * bare >, >>, < redirect to/from paste buffer
    * accepts abbreviated commands when unambiguous
    * `py` enters interactive Python console
    * test apps against sample session transcript (see example/example.py)

Useable without modification anywhere cmd is used; simply import cmd2.Cmd in place of cmd.Cmd.

Running `2to3 <http://docs.python.org/library/2to3.html>` against ``cmd2.py`` 
generates working, Python3-based code.

See docs at http://packages.python.org/cmd2/


