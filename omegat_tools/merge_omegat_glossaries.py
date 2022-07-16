# -*- coding: utf-8 -*-

'''
Create a single OmegaT glossary from several glossaries.

This script collects all entries from every OmegaT text format glossary in the specified folder, removes duplicates, and writes them to a single file.

The OmegaT glossary is simply a text file containing up to three fields: source term, target term and, optionally, additional notes or comments.

Entries are considered duplicates if they have identical source and target terms (including capitalization, hyphenation, and spacing). Entries with only a source term are discarded. However, entries with a source term and a note are retained even if they have no target term. If two entries have identical source and target terms, but one also has a supplementary note, the latter is preferred.
'''

###########################################################################
#
# Merge OmegaT Glossaries
# ---------------------------
# Version 0.2, released July 5, 2022
# Author: Philippe Tourigny
# License: GPL3+
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# The purpose of this script is to consolidate glossaries that were
# originally created independently but have a significant amount of
# overlapping content.
#
# TODO:
#   - Allow path to be passed as a command line argument
#   - Check that the files are valid glossary files
#
###########################################################################

import csv

import common


def get_glossary_settings():
    '''Load the glossary-related settings from the configuration file.'''

    settings = {'configpath':common.config['Paths']['glossaries'],
                'main':common.config['Files']['main_glossary'],
                'extensions':common.config['Files']['glossary_files'].replace(',', '')
               }
    
    return settings


def set_base_glossary_path():
    '''Assign the default path for glossary files'''

    configpath = glossary_settings['configpath']
    base_glossary_path = common.set_basepath(configpath)

    return base_glossary_path


def get_glossary_list(glossary_path):
    '''Retrieve the list of glossary files to merge from the glossary path'''

    # Syntax to retrieve more than one extension inspired by
    # this Stack Overflow answer: https://stackoverflow.com/a/57893015/8123921
    
    extensions = glossary_settings['extensions']
    glossary_list = (g for g in glossary_path.rglob('*')
                     if g.suffix in extensions)

    return glossary_list


def get_glossary_entries(glossary_file):
    '''Build a list of the entries in a glossary file.'''

    fields =['source', 'target', 'notes']
    skip = ('', None)

    entries = []

    with open(glossary_file, 'r', encoding='utf-8', newline='') as gf:
        greader = csv.DictReader(gf, fieldnames=fields, delimiter='\t')

        for line in greader:
            if line['target'] in skip and line['notes'] in skip:
                continue
            elif line['notes'] is not None:
                entry = (line['source'], line['target'], line['notes'])
            else:
                entry = (line['source'],line['target'],'')
            
            entries.append(entry)
    
    return entries


def remove_redundant_pairs(entries):
    '''Retain term pairs with a note if the exact same pair
       exists both with and without a note'''

    # Build list of duplicates differentiated only by the presence of a note.
    def find_duplicates(entries):

        pairs = [(term[0], term[1]) for term in entries]
        duplicates = []
        found = set()
        
        for pair in pairs:
            if pair in found:
                duplicates.append(pair)
            else:
                found.add(pair)
        
        return duplicates
    
    
    # Identify duplicate pairs that have no notes and should be discarded.
    def identify_discards(duplicates):

        discard = []

        for entry in entries:
            pair = (entry[0], entry[1])

            if pair in duplicates:
                if entry[2] == '':
                    discard.append(entry)
        
        return discard
    
    # Main function code starts here
    discard = identify_discards(find_duplicates(entries))
    glossary = [entry for entry in entries if not entry in discard]

    return glossary


def write_glossary(glossary):
    '''Write the final merged glossary to a new file.'''

    title = 'Enter name of file to save'
    glossary_files = [('Glossary file', glossary_settings['extensions'])]
    merged_name = common.get_save_file_name(glossary_path,
                                            glossary_files,
                                            title)
    merged_file = Path(glossary_path/merged_name)

    glossary_header=['# Glossary in tab-separated format -*- coding: utf-8 -*-']

    with open(merged_file, 'w', encoding='utf-8', newline='') as mf:
        gwriter = csv.writer(mf, delimiter='\t')

        gwriter.writerow(glossary_header)
        gwriter.writerows(glossary)


if __name__ == '__main__':

    # Retrieve configuration information for glossaries
    glossary_settings = get_glossary_settings()

    # Retrieve list of glossaries to merge
    askfolder = 'Select folder with glossary files'
    glossary_path = common.select_folder(set_base_glossary_path(), askfolder)

    glossary_list = get_glossary_list(glossary_path)

    # Build list of all entries from each glossary
    all_entries = []

    for glossary_file in glossary_list:
        entries = get_glossary_entries(glossary_file)
        all_entries.extend(entries)
    
    # Remove exact duplicates and any remaining redundant pairs
    all_entries = list(set(all_entries))
    merged_glossary = remove_redundant_pairs(all_entries)
    
    # Write merged glossary to a file
    write_glossary(merged_glossary)
