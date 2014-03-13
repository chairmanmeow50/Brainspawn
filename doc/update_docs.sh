#!/bin/bash
SOURCE_FOLDER="../brainspawn"
RST_FILES="source"

echo ">>> Cleaning old .rst files"
echo
rm -v "${RST_FILES}/modules.rst" "${RST_FILES}/brainspawn."* 

# Search source folder for new files. Creates basic .rst file for them that
# come with auto-doc methods and such
echo
echo ">>> Creating .rst files"
echo
sphinx-apidoc -o ${RST_FILES} ${SOURCE_FOLDER} || exit 1

echo
echo ">>> Creating html files"
echo
make html || exit 1

echo
echo ">>> Complete: open \"build/html/index.html\""
