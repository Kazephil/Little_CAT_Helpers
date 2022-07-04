# -*- coding: utf-8 -*-

'''
Copy memory and glossary files from memory projects to another folder.

A script to collect the "project_save.tmx" and "glossary.txt" files of
OmegaT projects and copy them to a user-selected centralized location
for ease of reference between projects or to facilitate their import
into other CAT tools.

The script creates subfolders with the original project name into a
user-selected central folder, and also renames both the memory and glossary
files to match the name of the project.
'''

###########################################################################
#
# Collect OmegaT Project Data
# ---------------------------
# Version 0.2, released July 4, 2022
# Author: Philippe Tourigny
# License: GPL3+
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Proper and more generalized rewrite of a quick script I'd put together
# when I had to collect the memories and glossaries from all my OmegaT
# projects so I could import them in the replacement tool my workplace
# decided to impose on us.
#
# TODO:
#   - Take glossaries other than the default 'glossary.txt" into account.
#   - Enable the customization of paths and files to copy.
#   - Allow users to create new directories from the folder selection
#     dialog.
###########################################################################

import shutil
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# Constants

# Default folder for Documents.
# Set to user home if there is no 'Documents' folder
DOCHOME = Path(Path.home()/'Documents')
if not DOCHOME.exists():
    DOCHOME = Path.home()

PROJECT = 'omegat.project'
MEMORY = 'omegat/project_save.tmx'
GLOSSARY = 'glossary/glossary.txt'


def select_folder(path, title):
    '''Present the user with a dialog to choose the folder they want to use.'''

    rootWin = tk.Tk()
    rootWin.attributes('-topmost', True)
    rootWin.withdraw()

    return filedialog.askdirectory(initialdir=path, title=title)


def make_project_list(searchpath):
    '''Build a list of all OmegaT projects in the search path,
       excluding duplicate data in the ".repositories" folder of
       team projects'''

    # In team projects, the '.repositories' subfolder is two levels
    # above the 'omegat.project' file, hence the need for two 'parent'
    # attributes.
    projects = [omt.parent for omt in searchpath.rglob(PROJECT)
                if not omt.parent.parent.stem == '.repositories']
                    
    return projects


def collate_project_data(projects):
    '''Get the project name and link it with the paths to its
       'project_save.tmx' and 'glossary.txt' files.'''

    project_data = {}
    for project in projects:
        # Retrieve the project name and the memory and glossary files
        project_name = project.stem
        
        project_data[project_name] = (Path(project, MEMORY),
                                       Path(project, GLOSSARY))

    return project_data


def copy_project_data(project_data):
    '''Create a subfolder for each project in the destination folder.
       Copy the corresponding memory and glossary files there, and
       rename them to match the project name.'''
       
    destination = Path(select_folder(DOCHOME, 'Select destination folder'))
       
    for name, data in project_data.items():

        # Create project subfolder
        project_folder = Path(destination/name)
        project_folder.mkdir(parents=True, exist_ok=True)

        for data_file in data:

            # Make sure the file is valid, give it the same name as the
            # project, and keep its original extension.
            if data_file.exists():
                new_file = Path(project_folder, name+data_file.suffix)
                print('Copying '+str(data_file)+' to '+' '+str(new_file))
                shutil.copy(data_file, new_file)

if __name__ == '__main__':
    projects_path = Path(select_folder(DOCHOME,
                         'Select the folder to search for OmegaT projects'))
                         
    projects = make_project_list(projects_path)
    project_data = collate_project_data(projects)
    copy_project_data(project_data)
