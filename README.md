Robodocset is a simple Python script which allow to generate [Docset](https://kapeli.com/docsets)
from [Robodoc](https://rfsber.home.xs4all.nl/Robo/) generated documentation.
This scrip is available under MIT license.

## Setting

Before you start, you will probably need to tweak script. Open it in any editor
and go to `types` definition. Key is part of file name to search for
documentation entries. Value is type of Docset entry which will be added to
the index. Thus `"subprograms": "Function"` means search file
*robo_subprograms.html* for documentation entries and add them as a
*Function* type of entries. For example, if you have file *robo_enums.html* and
you want add entries from there as *Enum* then add to this dictionary that
line:

`"enums": "Enum"`

All supported types of documentation you can find on Docset page. 

## Usage

Script require to work two arguments: first argument is a name of Docset which
will be generated and second is path (absolute or relative) to the directory
which contains ROBODoc generated documentation. Thus, generating Docset from
documentation in *docs* directory and with name *SomeDoc* will be looking that:

`./robodocset.py SomeDoc docs`

## After generation

Script of course can't generate icons for the docset. Additionally, you may
need to edit generated file *Info.plist* and add *docset.json* file in main
directory of the generated Docset.

----

And standard footer :)

That's all for now, and probably I forgot about something important ;) Feel
free to open Issue if you been have any question or problems with this script.

Bartek thindil Jasicki
