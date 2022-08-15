# -*- coding: utf-8 -*-

'''Create per translator TMX files from a base TMX file.

This script is used to parse TMX files from OmegaT projects involving more than one translator, and creates individual TMX files containing the translations made by each translator.

The user name of each translator and the name of the corresponding TMX file must be entered in the "Translators" section of the "omegat-tools.conf" file.

Requires:
  - Python 3.6 or higher (for f-strings)
  - lxml
'''

###########################################################################
#
# Segment Extractor
# ---------------------------
# Version 0.1, released August 15, 2022
# Author: Philippe Tourigny
# License: GPL3+
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Rebuilt implementation script targeted at OmegaT team projects originally
# designed to splits a team project TMX file into separate files containing
# the segments translated by each individual translator. The individual
# files are named using the two-letter target language code of the project
# and a two-letter translator identifier specified in the configuration file.
#
# The files can then be placed in the "tmx2source" subfolder of an OmegaT
# project tm folder to show each translator's original translation immediately
# below the source text during revision, for example.
#
# The script can also recognize revisers if they are defined in the
# configuration file, and add a note to a segment to indicate that it has been
# revised. The OmegaT option to apply coloring to segments with notes can
# then be used to quickly identify which segments have been revised.
#
# TODO:
#   - Automatically save the files to the "tmx2source" subfolder if a team
#     project tmx file is selected.
#   - Allow user selected individual TMX file names in addition to the
#     "tmx2source" file name format.
#   - Also accept a command line argument for the file to parse.
#   - Improve the revision notes to mark the differences between the original
#     and revised translations.
#   - Allow batch processing of multiple files.
#   - Enable the extraction of segments based on other criteria.
#   - Optionally output to a form of two-column table for review
#     outside a CAT tool.
###########################################################################

from lxml import etree

import common
from tmxhelpers import OmegaT_TMX


def set_tmxpath():
    '''Establish a starting path for the TMX file selection dialog.'''

    # Check whether user has defined a path for TMX files or projects 
    if common.config.has_option('Paths', 'tmxpath'):
        configpath = common.config['Paths']['tmxpath']
    else:
        configpath = common.config['Paths']['projects']

    tmxpath = common.set_basepath(configpath)

    return configpath


def parse_tmx_tree(tmxfile=None):
    '''Get the XML tree of the TMX file to parse'''

    def get_tmx_file():
        '''Get the TMX file to process.'''

        tmxpath = set_tmxpath()

        filetype=[('Translation memories', '*.tmx')]
        asktmx = 'Select TMX file'
        tmxfile = common.select_file(tmxpath, filetype, asktmx)

        return tmxfile
    
    # Ask the user to specify the file to parse if none was passed
    if tmxfile is None:
        tmxfile = get_tmx_file()
    
    tmxparser = etree.XMLParser(remove_blank_text=True)
    tmxtree = etree.parse(tmxfile, tmxparser)

    return tmxtree


def get_translator_list():
    '''Read list of translators and identifiers.

    The parser for the config file returns a list of tuples,
    which is converted to a dictionary. The list is then pruned
    down to the translators involved in the project from which
    the TMX file is taken'''

    translator_list = dict(common.config.items('Translators'))

    # Identify project translators whose work needs to be revised
    # based on the premise that a revised translation will have
    # a changeid that is not in the list of translators to revise.
    project_translators = set(BODY.xpath('//tuv/@changeid'))

    # Set up a dictionary containing the name and code of each
    # translator in the configuration file involved in the project.
    translators = {name:code for name, code in translator_list.items()
                   if name in project_translators}

    return translators


def prepare_tmx_containers():
    '''Set up a dictionary to hold each of the TMX files to revise.'''

    # Get the first two characters of the target language from the
    # translated tuv language attribute.
    tgtlang = BODY.xpath('//tuv[2]/@*[local-name() = "lang"]')[0][:2]
    sorted_tmxes = {}

    for translator in TRANSLATORS.keys():
        code = tgtlang + '-'+ TRANSLATORS[translator]
        sorted_tmxes[code] = OmegaT_TMX(header=HEADER.attrib,
                                        version=VERSION)    
    
    return sorted_tmxes


def sort_unrevised_tus():
    '''Sort unrevised translations into separate lists for each translator'''
    
    # Setup container for individual translator tmxes.
    sorted_tmxes = prepare_tmx_containers()

    # Retrieve all tuv elements containing a translation.
    # The translation is always in the second tuv element.
    translations = BODY.xpath('//tuv[2]')

    # Sort unrevised tuvs by translator
    for tuv in translations:
        creationid = tuv.attrib.get('creationid')
        changeid = tuv.attrib.get('changeid')
        
        if creationid in TRANSLATORS.keys() and changeid == creationid:
            translator = TRANSLATORS[changeid]
            code = [tmxid for tmxid in sorted_tmxes.keys()
                    if translator in tmxid].pop()
            tu = tuv.getparent()
            sorted_tmxes[code].add_tu(tu)
    
    return sorted_tmxes


def finalize_tmxdoc(tmxname, tmxcontent):
    '''Define the tmx tree for output to a file.'''
    
    # Set the full path and name for the TMX file.
    tmxpath = common.Path(TMXTREE.docinfo.URL).parent
    tmxfile = common.Path(tmxpath/tmxname).with_suffix('.tmx')
    
    tmxcontent.insert_alt_comment()
    tmxdoc = etree.ElementTree(tmxcontent.tmx)

    return (tmxfile, tmxdoc)


def write_tmx(tmxfile, tmxdoc):
    '''Output a TMX document to a file.'''

    tmxdoc.write(tmxfile, encoding='utf-8', pretty_print=True,
                 xml_declaration=True, doctype=DOCTYPE)


if __name__ == '__main__':

    # Parse the TMX file into an XML tree, and retrieve the main elements
    # and information needed to create the individual files.
    TMXTREE = parse_tmx_tree()
    TMXROOT = TMXTREE.getroot()
    HEADER, BODY = TMXROOT.getchildren()
    DOCTYPE = TMXTREE.docinfo.doctype
    VERSION = TMXROOT.attrib.get('version')
    

    # Get the list of translators whose work will be revised
    TRANSLATORS = get_translator_list()
    
    unrevised_translations = sort_unrevised_tus()
    
    for name, tmxcontent in unrevised_translations.items():
        unrevised_file, unrevised_doc = finalize_tmxdoc(name, tmxcontent)
        
        write_tmx(unrevised_file, unrevised_doc)