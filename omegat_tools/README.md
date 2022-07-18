# Little Tools for Working with OmegaT

The scripts in this directory are described below. They use the `pathlib` module, and therefore require Python 3.4 or higher, but have only been tried on Python 3.10. The scripts also share the limitation that symlinks to subfolders are not recognized.

## Collect OmegaT Project Data

### Overview

This script finds all OmegaT projects in a user-specified folder and its subfolders, and copies the default main memory ("project_save.tmx") and glossary ("glossary.txt") files to a destination folder selected by the user. The copying operation creates a subfolder for each project in that destination folder, renames both the memory and glossary files to match the project name, and copies then to the corresponding subfolder.

The original idea for the script came when my workplaced imposed a switch from OmegaT to a different CAT tool, and we were told to copy our existing memories and glossaries to a shared network folder.

The idea of manually going through various folders and subfolders, renaming each "project_save.tmx" and "glossary.txt" file to something more meaningful, and copying them to the shared folder was distinctively unappealing.

I managed to write an ugly, but functional script that did the bulk of the work. The script here is a rewrite based on the original idea.

### Usage and Requirements

Simply run the program from the command line or your favourite IDE. Select the folder from which you want to copy OmegaT project memories and glossaries the first time a dialog pops up. In the second dialog select the destination folder. The name of the file being copied is output to the console while the script is running.

### Limitations

1. The default OmegaT project subfolder hierarchy is assumed. Projects that use different names or locations for the subfolders in the OmegaT project hierarchy will not be recognized.
2. Glossaries other than the default "glossary.txt" file are not recognized or copied.
3. The destination folder for the files must be exist before the script is run because the folder selection dialog does not offer an option to create a new directory.

### Possible Improvements

Since I currently only use OmegaT on occasion for personal projects, progress on improvements is likely to be slow, but listing them here will ensure the ideas are not forgotten.

1. Copy other reference glossaries in addition to the default glossary file.
2. Accommodate user-defined project structures directory names, and choice of files to copy.
3. Allow users to create the destination directory from the folder selection dialog.
4. Provide an option to copy the memories and glossaries to a central memory or glossary folder rather than to individual subfolders named after the project.

## Merge Glossaries

### Overview

This script reads all glossary files in the selected folder (and subfolders), removes any duplicates, and generates a file containing the "# Glossary in tab-separated format -\*- coding: utf-8 -\*-" OmegaT glossary file header, as well as every unique entry from each glossary file in the selected folder.

Although OmegaT only recognizes the _\*.txt_ and _\*.utf8_ extensions, the script has been extended to also accept files with the _\*.csv_ or _\*.tsv_ extensions to accommodate merging files created outside OmegaT that follow the same glossary structure. Entries with data in at least two of the three available fields are retained, and lines with data in only one field are discarded.

If different glossaries contain the same pair of source and target terms, but one pair also has a note, the pair containing the note is retained and the other is discarded.

### Usage and Requirements

Upon executing the program, select the folder that contains the glossaries to merge. When the next dialog comes up, enter the name you want to give the merged glossary file, including the extension. You can optionally change the directory as well.

### Limitations

1. The script assumes that the input files all match the OmegaT text glossary format, namely "source term", "target term", and "notes" separated by tabs. Any files with more columns, a different column order, or other formatting differences are likely to produce strange and unpredictable results.
2. Since the script is intended to produce an OmegaT glossary, the inclusion of the OmegaT glossary file header is hardcoded and can currently only be removed by updating the code.

### Possible Improvements

I've listed a few random ideas below, lest I forget them later. I'm not entirely sure how I could implement the first one, and the last one should perhaps be a small separate script rather than an extension of this one.

1. Check the files in the selected directory and only process those that are valid glossary-format files.
2. Provide an option to search only specific subfolders
3. Allow the user to choose whether to include the glossary header in the final file.
4. Add options to sort the entries (by source, target, or entry length, for example) before writing the merged glossary file.
5. Extend the concept to merge the _learned_words.txt_ and _ignored_words.txt_ files from multiple OmegaT projects.
