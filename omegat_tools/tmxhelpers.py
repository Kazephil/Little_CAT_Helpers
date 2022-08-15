# -*- coding: utf-8 -*-

from lxml import etree

class TMX:
    '''Base class to define and manipulate simple TMX documents.'''

    # Default values
    default_doctype = '<!DOCTYPE tmx SYSTEM "tmx14.dtd">'
    default_version = '1.4'
    default_header = {'creationtool': 'Segment Extractor',
                      'o-tmf': 'Unknown',
                      'adminlang': 'EN-US',
                      'datatype': 'plaintext',
                      'creationtoolversion': '0.1',
                      'segtype': 'sentence',
                      'srclang': 'JA'
                     }


    def __init__(self, header=default_header, version=default_version):
        self.tmx = etree.Element('tmx', attrib={'version': version})
        self.header = etree.SubElement(self.tmx, 'header', header)
        self.body = etree.SubElement(self.tmx, 'body')

    
    def add_tu(self, tu):
        '''Add a tu element to the TMX document.'''

        # Todo: add code to ensure the tu is valid
        self.body.append(tu)


class OmegaT_TMX(TMX):
    '''Class for OmegaT-specific TMX documents.'''

    def __init__(self, header=TMX.default_header, version='1.4'):
        super().__init__(header, version)
        self.default_trans = etree.Comment('Default translations')
        self.body.append(self.default_trans)

    
    def find_alternative_translations(self):
        '''Check for alternative translations in the TMX document'''

        alt_expr = '(//tu/prop[@type="file"])[1]'
        prop_types = ['id', 'prev', 'next']
        check_alt = self.body.xpath(alt_expr)
        
        if len(check_alt) > 0:
            prop = check_alt[0].getnext().attrib.get('type')
            if prop in prop_types:
                return check_alt[0].getparent()
            
            

    def insert_alt_comment(self):
        '''Insert the alternative translation comment in the TMX document.'''
        
        self.alt_trans =etree.Comment('Alternative translations')

        # alt_expr = 'count(//tu/prop)>=3'
        
        first_alt = self.find_alternative_translations()
        if first_alt is not None:            
            first_alt.addprevious(self.alt_trans)
        else:
            self.body.append(self.alt_trans)


class TMXfile():
    pass