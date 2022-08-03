# -*- coding: utf-8 -*-

'''Module that defines file-related dialogs used across scripts.'''

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from configparser import ConfigParser

# Constants
CONFIGFILE = Path('./config/omegat-tools.conf')
USER_HOME = Path.home()
DEFAULT_DOCHOME = Path(USER_HOME/'Documents')

def read_config(configfile):
    '''Load the configuration file'''

    parser = ConfigParser()
    parser.read(configfile, encoding='utf-8')
    
    return parser


def set_basepath(configpath):
    '''Define the default starting path for documents.
       
       Each tool reads the applicable configuration path from the
       configuration file and passes it to this function.    
    '''

    # Give priority to path set in config file, if valid.
    # If not, use the user's 'Documents' folder if it exists,
    # and the user folder if not, as a default.

    candidates = [Path(configpath), DEFAULT_DOCHOME, USER_HOME]
    basepath = None
    
    # Read each candidate path in term, and set the first valid path
    # as the basepath
    while basepath is None:
        if candidates[0].exists():
            basepath = candidates[0]
        else:
            candidates.pop(0)
    
    return basepath


def set_root_window():
    '''Define a root window file dialog.'''
    
    rootWin = tk.Tk()
    rootWin.attributes('-topmost', True)
    rootWin.withdraw()


def select_folder(basepath, title):
    '''Ask user to choose a folder.'''

    set_root_window()
    selected_folder = Path(filedialog.askdirectory(initialdir=basepath,
                                                   title=title))

    return selected_folder


def select_file(basepath, title):
    '''Ask the user to select a single file'''

    set_root_window()
    selected_file = Path(filedialog.askopenfilename(initialdir=basepath,
                                                     title=title))

    return selected_file


def get_save_file_name(basepath, filetypes, title):
    '''Ask for the name of the file to save.'''

    set_root_window()
    save_file_name = Path(filedialog.asksaveasfilename(initialdir=basepath,
                          filetypes = filetypes, title=title))

    return save_file_name


config = read_config(CONFIGFILE)