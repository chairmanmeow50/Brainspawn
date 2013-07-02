############################################
#                                          #
#  Brainspqwn Sphinx Documentation Readme  #
#                                          #
############################################

How to: 
#######

Create HTML documentation
-------------------------
    1. > cd doc
    2. > make html

Document new python files
-------------------------
    The following commands should automatically detect all python files and create 
    "*.rst" files for them. If this doesn't work, try replacing the source 
    parameter (the last one) with the relative path to the specific file.

    1. > cd doc
    2. > sphinx-apidoc -o rst/ ../src/

Modify page for an existing file
--------------------------------
    Simply edit the corresponding ___.rst file.
