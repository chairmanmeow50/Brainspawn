############################################
#                                          #
#  Brainspqwn Sphinx Documentation Readme  #
#                                          #
############################################


1. Create any missing .rst files for new source files
--------------------------------------------------
    The following commands should automatically detect all python files and create 
    "*.rst" files for them.

    1. > cd doc
    2. > sphinx-apidoc -o source ../brainspawn

2. Add additional info for a python file
----------------------------------------

    1. Edit the corresponding .rst file.

3. Update/Create HTML documentation
-------------------------
    * Ensure source/conf.py:21 "sys.path.insert(...)" line is set to "sys.path.insert(0, os.path.abspath('../..'))" This allows autodoc to find our source code to pull docstrings
    
    1. > cd doc
    2. > make html
