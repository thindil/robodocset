#!/usr/bin/env python3
# Copyright (c) 2019-2020 Bartek thindil Jasicki <thindil@laeran.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sqlite3
import glob
import sys
import shutil

# Set documentation directory and docset name
if len(sys.argv) == 3:
    docname = sys.argv[1]
    docsdir = sys.argv[2]
else:
    print("You must enter exactly two arguments: name of the docset to create and relative or absolute path to the directory where ROBODoc generated documentation is.")
    sys.exit(0)

# Files and types of entries which will be added to the index. Key is part of
# file name to search for documentation entries. Value is type of Docset
# entry which will be added to the index. Thus "subprograms": "Function" means
# search file "robo_subprograms.html" for documentation entries and add them
# as a "Function" type of entries. If you have other setting for the names
# of files or you want to change types of Docset entries, feel free to edit
# this.
types = {"subprograms": "Function",
         "packages": "Package",
         "exceptions": "Exception",
         "variables": "Variable",
         "types": "Type"}

# Copy documentation to proper directory
try:
    shutil.copytree(docsdir, docname + ".docset/Contents/Resources/Documents")
except shutil.Error as error:
    print('Directory not copied. Error: %s' % error)
except OSError as error:
    print('Directory not copied. Error: %s' % error)

# Fill documentation index with entries
conn = sqlite3.connect(docname + '.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()
try:
    cur.execute('DROP TABLE searchIndex;')
except:
    pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')

for filename in glob.glob(docname + ".docset/Contents/Resources/Documents/robo_*.html"):
    with open(filename) as fn:
        content = fn.readlines()
    i = 0
    while i < len(content):
        line = content[i].strip()
        pos = line.find("class=\"indexitem\"")
        if pos > -1:
            endpos = line.find("</a>", pos)
            pathstart = line.find("<a href=") + 9
            path = line[pathstart:line.find("\"", pathstart + 1)]
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                        (line[(pos + 19):endpos], types[filename[(len(docname) + 42):-5]], path))
        i += 1

conn.commit()
conn.close()

# Create plist file needed by Docset
pfile = open(docname + ".docset/Contents/Info.plist", "w")
pfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
pfile.write("<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
pfile.write("<plist version=\"1.0\">\n")
pfile.write("<dict>\n")
pfile.write("<key>C:FBundleIdentifier</key>\n")
pfile.write("<string>" + docname.lower() + "</string>\n")
pfile.write("<key>CFBundleName</key>\n")
pfile.write("<string>" + docname + "</string>\n")
pfile.write("<key>DocSetPlatformFamily</key>\n")
pfile.write("<string>" + docname.lower() + "</string>\n")
pfile.write("<key>isDashDocset</key>\n")
pfile.write("<true/>\n")
pfile.write("<key>dashIndexFilePath</key>\n")
pfile.write("<string>index.html</string>\n")
pfile.write("</dict>\n")
pfile.write("</plist>\n")
pfile.close()
