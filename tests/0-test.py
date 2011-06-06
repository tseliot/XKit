#       0-test.py -- Test suite for xorgparser
#       
#       Copyright 2008 Alberto Milone <albertomilone@alice.it>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from xkit import xorgparser
from xkit.xorgparser import *
import sys
import unittest
import os
import logging
import settings
import tempfile
import copy

source = settings.inputFile
destination = settings.outputDir
destinationFile = os.path.join(settings.outputDir, 'xkittest-0.txt')
tempFile = os.path.join(destination, 'tmp')

section = 'Device'

class XorgParserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.parser = xorgparser.Parser(source)
    
    def tearDown(self):
        self.parser.comments.insert(0, '\n-----' + self.this_function_name + '-----\n')
        self.parser.write(destinationFile, test=True)
        try:
            os.remove(tempFile)
        except(OSError, IOError):
            pass
    
    def test_fill_identifiers(self):
        '''
        def __fill_identifiers(self):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKit Screen'
        self.parser.make_section(section, identifier)
        
        fullSection = self.parser.globaldict[section]
        found1 = False
        found2 = False
        for position in fullSection:
            lines = fullSection[position]
            for line in lines:
                if line.find(identifier) != -1 and \
                line.lower().find('identifier') != -1:
                    found1 = True
                    break
        
        ids = self.parser.identifiers[section]
        
        for elem in ids:
            if elem[0] == identifier:
                found2 = True
                break
        
        self.failUnless(found1 == True and found2 == True, 'Not all the identifiers were returned')

    def test_get_identifier1(self):
        '''
        def get_identifier(self, section, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier1 = 'XKit Screen'
        position1 = self.parser.make_section(section, identifier1)
        identifier2 = self.parser.get_identifier(section, position1)
        
        self.failUnless(identifier1 == identifier2, 
                        'The identifier was not correctly retrieved')
    
    def test_get_identifier2(self):
        '''
        def get_identifier(self, section, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        self.parser = xorgparser.Parser(None)
        
        
        self.assertRaises(SectionException,
                      self.parser.get_value, 'Device', 'Identifier', 1)
        
        self.assertRaises(IdentifierException,
                      self.parser.get_identifier, 'Device', 0)

    def testGetDuplicateOptions(self):
        '''
        def get_duplicate_options(self, section, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Device Section'
        option = 'TestOption1'
        value1 = '0'
        value2 = '1'
        position = self.parser.make_section(section, identifier=identifier)
        
        self.parser.add_option(section, option, value1, option_type='Option', position=position)
        
        '''
        add_option doesn't allow the creation of duplicates
        '''
        option2 = '\t' + 'Option' + '\t' + option + '\t\t"' + value2 + '"\n'
        self.parser.globaldict[section][position].append(option2)
        
        duplicates = self.parser.get_duplicate_options(section, position)
        
        self.failUnless(option in duplicates, 'Duplicates cannot be found!')

    def testCheckDuplicateOptions(self):
        '''
        def check_duplicate_options(self):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        self.parser = xorgparser.Parser(None)
        
        section = 'Device'
        identifier = 'XKit Device Section'
        option = 'TestOption1'
        value1 = '0'
        value2 = '1'
        position = self.parser.make_section(section, identifier=identifier)
        
        self.parser.add_option(section, option, value1, option_type='Option', position=position)
        
        option2 = '\t' + 'Option' + '\t' + option + '\t\t"' + value2 + '"\n'
        
        '''
        add_option doesn't allow the creation of duplicates
        '''
        self.parser.globaldict[section][position].append(option2)
        
        duplicates = self.parser.check_duplicate_options()
        
        self.failUnless(option in duplicates[section][position], 'Duplicates can still be found!')
    
    def testGetDuplicateSections(self):
        '''
        def get_duplicate_sections(self):
        
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        section = 'Screen'
        identifier1 = 'XKit Screen test1'
        
        pos = self.parser.make_section(section, identifier=identifier1)
        
        '''
        create a duplicate section without using add_option()
        '''
        self.parser.globaldict[section][pos+1] = ['\tIdentifier\t\t"' + identifier1 + '"\n']
        self.parser.identifiers[section].append((identifier1, pos+1))#ADD to identifiers
        duplicates = self.parser.get_duplicate_sections()
        
        self.failUnless(identifier1 in duplicates[section],
                        'Duplicates sections cannot be retrieved correctly!')

    def test_is_section1(self):
        '''
        def is_section(self, section, identifier):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKit Screen'
        position = self.parser.make_section(section, identifier)
        
        status1 = self.parser.is_section(section, identifier)
        
        status2 = False
        sect = self.parser.globaldict[section][position]
        for line in sect:
            if line.find(identifier) != -1:
                status2 = True
                break
        
        self.failUnless(status2 == True and status1 == status2, 
                        'The existence of the section was not tested correctly')

    def test_is_section2(self):
        '''
        def is_section(self, section, identifier):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKit Screen'
        position = self.parser.make_section(section, identifier)
        
        status1 = self.parser.is_section(section, position=position)
        
        status2 = False
        sect = self.parser.globaldict[section][position]
        for line in sect:
            if line.find(identifier) != -1:
                status2 = True
                break
        
        self.failUnless(status2 == True and status1 == status2, 
                        'The existence of the section was not tested correctly')

    def test_add_option1(self):
        '''
        def add_option(self, section, option, value, option_type=None, position=None, reference=None):
        '''
        
        self.this_function_name = sys._getframe().f_code.co_name
        
        option = 'TestOption'
        value = 'Ok'
        #position = 0
        found = False
        self.parser.add_option(section, option, value, option_type=None, position=None, reference=None)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == True, 'Option not added!')
        
        
    def test_add_option2(self):
        '''
        def add_option(self, section, option, value, option_type=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        option = 'TestOption'
        value = 'Ok'
        #position = 0
        found = False
        self.parser.add_option(section, option, value, option_type="Option", position=None, reference=None)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == True, 'Option not added!')
        
    def test_add_option3(self):
        '''
        def add_option(self, section, option, value, option_type=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        option = 'TestOption'
        value = 'Ok'
        position = 0
        found = False
        self.parser.add_option(section, option, value, option_type=None, position=None, reference=None)
        lines = self.parser.globaldict[section][position]
        for line in lines:
            if line.find(option) != -1:
                found = True
        self.failUnless(found == True, 'Option not added!')
        
    def test_add_option4(self):
        '''
        def add_option(self, section, option, value, option_type=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        option = 'TestOption'
        value = 'Ok'
        #position = 0
        found = False
        self.parser.add_option(section, option, value, option_type=None, position=None, reference=True)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == True, 'Option not added!')
        
    def test_add_option5(self):
        '''
        def add_option(self, section, option, value, option_type=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        option = 'DefaultDepth'
        value = '24'
        #position = 0
        found = False
        
        screen = self.parser.make_section('Screen', identifier='Xkit Screen Device 5')
        
        self.parser.add_option(section, option, value, position=screen, prefix='')
        lines = self.parser.globaldict[section][screen]
        for line in lines:
            if line.find(option) != -1:
                found = True
                #print line
        self.failUnless(found == True, 'Option not added!')
        
        
    def test_remove_option1(self):
        '''
        def remove_option(self, section, option, value=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'Identifier'
        found = False
        self.parser.remove_option(section, option, value=None, position=None, reference=None)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == False, 'Option not removed!')
    
    def test_remove_option2(self):
        '''
        def remove_option(self, section, option, value=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'Identifier'
        value = 'Configured Video Device'
        found = False
        self.parser.remove_option(section, option, value=None, position=None, reference=None)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1 and line.find(value) != -1:
                    found = True
                    #print line
            self.failUnless(found == False, 'Option not removed!')
    
    def test_remove_option3(self):
        '''
        def remove_option(self, section, option, value=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'Identifier'
        reference = True
        found = False
        self.parser.remove_option(section, option, value=None, position=None, reference=None)
        for position in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == False, 'Option not removed!')
        
    def test_make_section1(self):
        '''
        def make_section(self, section, identifier=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Extensions'
        before = len(self.parser.globaldict[section])
        position = self.parser.make_section(section, identifier=None)
        
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
    
    def test_make_section2(self):
        '''
        def make_section(self, section, identifier=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Video Device'
        position = self.parser.make_section(section, identifier=identifier)
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
        
        found = False
        lines = self.parser.globaldict[section][position]
        for line in lines:
            if line.find('Identifier') != -1 and line.find(identifier) != -1:
                found = True
                #print line
        self.failUnless(found == True, 'Section not created correctly!')

    def test_make_section3(self):
        '''
        def make_section(self, section, identifier=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Extensions'
        position = self.parser.make_section(section, identifier=None)
        
        sect = self.parser.globaldict[section].get(position)
        
        self.failUnless(sect != None, 
                        'The section was not created')
    
    def test_make_section4(self):
        '''
        def make_section(self, section, identifier=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Video Device'
        position = self.parser.make_section(section, identifier=identifier)
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
        
        found = False
        lines = self.parser.globaldict[section][position]
        for line in lines:
            if line.find('Identifier') != -1 and line.find(identifier) != -1:
                found = True
                #print line
        self.failUnless(found == True, 'Section not created correctly!')
        
        ids = self.parser.identifiers[section]
        found = False
        for elem in ids:
            if elem[0] == identifier:
                found = True
                break
        
        self.failUnless(found == True, 'Identifiers list not updated!')

    def test_add_reference1(self):
        '''
        def add_reference(self, section, reference, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='ServerLayout'
        reference='Screen'
        identifier = 'XKit Screen Device'
        #position=0 #the first ServerLayout section
        self.parser.add_reference(section, reference, identifier, position=None)
        
        found = False
        for pos in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][pos]
            for line in lines:
                if line.find(reference) != -1 and line.find(identifier) != -1:
                    found = True
                    #print line
            self.failUnless(found == True, 'Reference not added!')
    
    def test_add_reference2(self):
        '''
        def add_reference(self, section, reference, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='ServerLayout'
        reference='Screen'
        identifier = 'XKit Screen Device'
        position=0 #the first ServerLayout section
        
        if len(self.parser.globaldict[section]) == 0:
            position = self.parser.make_section(section, identifier='Default layout')
            
        self.parser.add_reference(section, reference, identifier, position=position)
        
        found = False
        lines = self.parser.globaldict[section][position]
        for line in lines:
            if line.find(reference) != -1 and line.find(identifier) != -1:
                found = True
                #print line
        self.failUnless(found == True, 'Reference not added!')
    
    def test_remove_reference1(self):
        '''
        def remove_reference(self, section, reference, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='ServerLayout'
        reference='Screen'
        identifier = 'XKit Screen Device'
        #position=0 #the first ServerLayout section
        
        if len(self.parser.globaldict[section]) == 0:
            position = self.parser.make_section(section, identifier='Default layout')
        
        self.parser.add_reference(section, reference, identifier, position=None)
        self.parser.remove_reference(section, reference, identifier, position=None)
        
        found = False
        for pos in self.parser.globaldict[section]:
            lines = self.parser.globaldict[section][pos]
            for line in lines:
                if line.find(reference) != -1 and line.find(identifier) != -1:
                    found = True
                    #print line
            self.failUnless(found == False, 'Reference not removed!')
    
    def test_remove_reference2(self):
        '''
        def remove_reference(self, section, reference, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='ServerLayout'
        reference='Screen'
        identifier = 'XKit Screen Device'
        position=0 #the first ServerLayout section
        
        if len(self.parser.globaldict[section]) == 0:
            position = self.parser.make_section(section, identifier='Default layout')
        
        self.parser.add_reference(section, reference, identifier, position=position)
        self.parser.remove_reference(section, reference, identifier, position=position)
        
        found = False
        lines = self.parser.globaldict[section][position]
        for line in lines:
            if line.find(reference) != -1 and line.find(identifier) != -1:
                found = True
                #print line
        self.failUnless(found == False, 'Reference not removed!')
    
    
    def test_get_references1(self):
        '''
        def get_references(self, section, position, reflist=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='Screen'
        position=0 #the first ServerLayout section
        reference= 'Device'
        identifier = 'XKit Video Device'
        
        screen = self.parser.make_section('Screen', identifier=identifier.replace('Video', 'Screen'))
        device = self.parser.make_section(reference, identifier=identifier)
        
        #if len(self.parser.globaldict[section].setdefault(position, [])) == 0:
        self.parser.add_reference(section, reference, identifier, position=screen)
            
        references = self.parser.get_references(section, screen, reflist=None)
        self.failUnless(len(references) > 0, 'No list of References can be retrieved!')
    
    def test_get_references2(self):
        '''
        def get_references(self, section, position, reflist=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section='Screen'
        position=0 #the first ServerLayout section
        reference='Device'
        identifier = 'XKit Video Device'
        reflist=['Device']
        if len(self.parser.globaldict[section].setdefault(position, [])) == 0:
            self.parser.add_reference(section, reference, identifier, position=position)
        references = self.parser.get_references(section, position, reflist=reflist)
        self.failUnless(len(references) > 0, 'No list of References can be retrieved!')
    
    def test_make_subsection1(self):
        '''
        def make_subsection(self, section, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        times = 5
        for pos in range(times):
            self.parser.globaldict[section].setdefault(pos, [])
        self.parser.make_subsection(section, identifier)
        '''
        self.globaldict['SubSection'] =
                    {0: {'section': 'Screen', 'identifier': 'Display', 
                    'position': 0, 'options': [option1, option2, etc.], 
                    etc.}
        '''
        
        found = 0
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('section') == section and \
                subsection.get('identifier') == identifier:
                found += 1
        #print self.parser.globaldict['SubSection']
        #print 'found =', found, '; times =', times
        self.failUnless(found >= times, 'The subsections were not created!')
    
    def test_make_subsection2(self):
        '''
        def make_subsection(self, section, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        position = 0
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.make_subsection(section, identifier, position=position)
        '''
        self.globaldict['SubSection'] =
                    {0: {'section': 'Screen', 'identifier': 'Display', 
                    'position': 0, 'options': [option1, option2, etc.], 
                    etc.}
        '''
        found = False
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('section') == section and \
                subsection.get('identifier') == identifier and \
                subsection.get('position') == position:
                found = True
        self.failUnless(found == True, 'The subsection was not created!')
    
    
    def test_remove_subsection1(self):
        '''
        def remove_subsection(self, section, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        
        times = 5
        for pos in range(times):
            self.parser.globaldict[section].setdefault(pos, [])
            self.parser.make_subsection(section, identifier, position=pos)
        
        self.parser.remove_subsection(section, identifier)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            self.failUnless(subsection.get('identifier') != identifier or \
            subsection.get('section') != section,
            'The subsections were not removed!')
    
    def test_remove_subsection2(self):
        '''
        def remove_subsection(self, section, identifier, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        position = 0
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.make_subsection(section, identifier, position=position)
        self.parser.remove_subsection(section, identifier, position=position)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            self.failUnless(subsection.get('identifier') != identifier or \
            subsection.get('section') != section or \
            subsection.get('position') != position,
            'The subsections were not removed!')
    
    
    
    def test_add_suboption1(self):
        '''
        def add_suboption(self, section, identifier, option, value, option_type=None, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        #position = 0
        option = 'Virtual'
        value = '2048 2048'
        
        times = 5
        for pos in range(times):
            self.parser.globaldict[section].setdefault(pos, [])
        self.parser.make_subsection(section, identifier)
        
        self.parser.add_suboption(section, identifier, option, value)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1 and line.find(value) != -1:
                        found = True
                self.failUnless(found == True, 'Option not added to all the Subsections')
        
    def test_add_suboption2(self):
        '''
        def add_suboption(self, section, identifier, option, value, option_type=None, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        position = 0
        option = 'Virtual'
        value = '2048 2048'
        
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.make_subsection(section, identifier, position=position)
        
        self.parser.add_suboption(section, identifier, option, value, position=position)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section and \
            subsection.get('position') == position:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1 and line.find(value) != -1:
                        found = True
                self.failUnless(found == True, 'Option not added to the Subsection')
        
    def test_add_suboption3(self):
        '''
        def add_suboption(self, section, identifier, option, value, option_type=None, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        #position = 0
        option = 'Virtual'
        value = '2048 2048'
        option_type = 'Option'
        
        times = 5
        for pos in range(times):
            self.parser.globaldict[section].setdefault(pos, [])
        self.parser.make_subsection(section, identifier)
        
        self.parser.add_suboption(section, identifier, option, value, option_type=option_type)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1 and line.find(value) != -1 and \
                    line.find(option_type) != -1:
                        found = True
                self.failUnless(found == True, 'Option not added to all the Subsections')
    
    
    def test_remove_suboption1(self):
        '''
        def remove_suboption(self, section, identifier, option, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        #position = 0
        option = 'Virtual'
        value = '2048 2048'
        option_type = 'Option'
        
        times = 5
        for pos in range(times):
            self.parser.globaldict[section].setdefault(pos, [])
        self.parser.make_subsection(section, identifier)
        
        self.parser.add_suboption(section, identifier, option, value, option_type=option_type)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1 and line.find(value) != -1:
                        found = True
                self.failUnless(found == True, 'Option not added to all the Subsections')
        
        #self.parser.write(sys.stderr)
        
        self.parser.remove_suboption(section, identifier, option)
        
        #self.parser.write(sys.stderr)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1:
                        found = True
                self.failUnless(found == False, 'Option not removed from all the Subsections')

    def test_remove_suboption2(self):
        '''
        def remove_suboption(self, section, identifier, option, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        position = 0
        option = 'Virtual'
        value = '2048 2048'
        
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.make_subsection(section, identifier, position=position)
        
        self.parser.add_suboption(section, identifier, option, value, position=position)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section and \
            subsection.get('position') == position:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1 and line.find(value) != -1:
                        found = True
                self.failUnless(found == True, 'Option not added to the Subsection')
        
        self.parser.remove_suboption(section, identifier, option, position=position)
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('position') == position and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1:
                        found = True
                self.failUnless(found == False, 'Option not removed from the Subsection')
    
    def test_get_value1(self):
        '''
        def get_value(self, section, option, position, identifier=None, sect=None, reference=None):
        
            * When dealing with a Section:
                section= e.g. 'Screen', 'Device', etc.
                option= the option
                position= e.g. 0 (i.e. the first element in the list of Screen
                          sections)
                reference= used only by get_references()
            
            * When dealing with a SubSection:
                section= 'SubSection' (this is mandatory)
                option= the option
                position= e.g. 0 would mean that the subsection belongs to 
                          the 1st item of the list of, say, "Screen" sections.
                          (i.e. the first element in the list of Screen 
                          sections)
                          ["position" is a key of an item of the list of 
                          subsections see below]
                
                identifier= the name of the subsection e.g. 'Display'
                sect = the 'section' key of an item of the list of 
                       subsections e.g. the "Display" subsection can be 
                       found in the "Screen" section ('sect' is the latter)
                       
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'TestOption'
        value = 'Ok'
        position = 0
        option_type = 'Option'
        
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.add_option(section, option, value, option_type=option_type, position=position)
        
        result = self.parser.get_value(section, option, position)
        self.failUnless(result == value, 'Incorrect value retrieved')
    
    
    
    def test_get_value2(self):
        '''
        def get_value(self, section, option, position, identifier=None, sect=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'TestOption'
        value = 'Ok'
        position = 0
        option_type = None
        reference = True
        
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.add_option(section, option, value, option_type=option_type,
                              position=position, reference=reference)
        
        result = self.parser.get_value(section, option, position)
        self.failUnless(result == value, 'Incorrect value retrieved')
    
    
    def test_get_value3(self):
        '''
        def get_value(self, section, option, position, identifier=None, sect=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKitDisplay'
        option = 'TestOption'
        value = 'Ok'
        position = 0
        option_type = 'Option'
        
        self.parser.globaldict[section].setdefault(position, [])
        self.parser.add_suboption(section, identifier, option, value,
                                 option_type=option_type, position=position)
        
        sect = section
        section = 'SubSection'
        
        result = self.parser.get_value(section, option, position,
                                      identifier=identifier, sect=sect)
        
        self.failUnless(result == value, 'Incorrect value retrieved')
    
    def test_get_value4(self):
        self.this_function_name = sys._getframe().f_code.co_name
        self.parser = xorgparser.Parser(None)
 
        self.assertRaises(SectionException,
                      self.parser.get_value, 'Device', 'Identifier', 1)
    
    def test_get_value5(self):
        self.this_function_name = sys._getframe().f_code.co_name
        self.parser = xorgparser.Parser(None)
        device = self.parser.make_section('Device', identifier='Default Device')
        self.assertRaises(OptionException,
                      self.parser.get_value, 'Device', 'Driver', device)
    
    def testIntegrity1(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screen"\n\
\tIdentifier\t"Default Screen"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
\tSubSection "Display"\n\
\tEndSubSeection\n\
EndSection\n\n\
Section "InputDevice"\n\
\tIdentifier\t"Generic Keyboard"\n\
\tDriver\t\t"kbd"\n\
\tOption\t\t"XkbRules"\t"xorg"\n\
\tOption\t\t"XkbModel"\t"pc105"\n\
\tOption\t\t"XkbLayout"\t"it"\n\
EndSection\n'
        
        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)
    
    def testIntegrity2(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screen"\n\
\tIdentifier\t"Default Screen"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
\tSubSecttttion "Display"\n\
\tEndSubSection\n\
EndSection\n\n\
Section "InputDevice"\n\
\tIdentifier\t"Generic Keyboard"\n\
\tDriver\t\t"kbd"\n\
\tOption\t\t"XkbRules"\t"xorg"\n\
\tOption\t\t"XkbModel"\t"pc105"\n\
\tOption\t\t"XkbLayout"\t"it"\n\
EndSection\n'
        
        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity3(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screeen"\n\
\tIdentifier\t"Default Screen"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
\tSubSection "Display"\n\
\tEndSubSection\n\
EndSection\n\n\
Section "InputDevice"\n\
\tIdentifier\t"Generic Keyboard"\n\
\tDriver\t\t"kbd"\n\
\tOption\t\t"XkbRules"\t"xorg"\n\
\tOption\t\t"XkbModel"\t"pc105"\n\
\tOption\t\t"XkbLayout"\t"it"\n\
EndSection\n'
        
        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity4(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screeen"\n\
\tIdentifier\t"Default Screen"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
\tSubSeection "Display"\n\
\tEnwwdSubSection\n\
EndSection\n\n\
Section "InputDevice"\n\
\tIdentifier\t"Generic Keyboard"\n\
\tDriver\t\t"kbd"\n\
\tOption\t\t"XkbRules"\t"xorg"\n\
\tOption\t\t"XkbModel"\t"pc105"\n\
\tOption\t\t"XkbLayout"\t"it"\n\
EndSecttion\n'
        
        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity5(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screen"\n\
\tIdentifier\t"Default Screen"\n\
\tSection\t"Device"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
EndSecttion\n'
        
        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity6(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = '\
Section "Screen"\n\
\tIdentifier\t"Default Screen"\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
\t\tSubSection\t\t"Display"\n\
EndSection\n\n\
Section "Screen"\n\
\tIdentifier\t"Default Screen"\n\
\tEndSubSection\n\
\tMonitor\t\t"Configured Monitor"\n\
\tDevice\t\t"Configured Video Device"\n\
EndSection\n'

        a = open(tempFile, 'w')
        a.write(confFile)
        a.close()
 
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity7(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''



Section "Screen"
    Identifier  "MGA 2"
    Device "card1"
EndSection

Section "Screen"
    Identifier  "MGA 3"
    Device "card2"
EndSection
''', file=confFile)

        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity8(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Screen"
    Identifier  "New Screen Device"
EndSection

Section "ServerLayout"
    Identifier "Another Layout"
    Option "Whatever"
    Screen "New Screen Device" 0 0
EndSection
''', file=confFile)
        
        confFile.close()
        
        valid = True
        try:
            self.parser = xorgparser.Parser(tempFile)
        except ParseException:
            valid = False
        
        self.failUnless(valid == True, 'the xorg.conf should be considered valid')

    def testIntegrity9(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Screen"
    Identifier  "New Screen Device"
EndSection

Section "Device"
    Identifier "My device"
EndSection

Section "ServerLayout"
    Identifier "Another Layout"
    Option "Whatever"
    Screen "New Screen Device" 0 0
    InputDevice "My device"
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException, xorgparser.Parser, tempFile)

    def testIntegrity10(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Screen"
    Identifier  "New Screen Device"
EndSection

Section "Device"
    Option "FakeOption" "True"
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException, xorgparser.Parser, tempFile)

    def testIntegrity11(self):
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "ServerLayout"
    
    # Uncomment if you have a wacom tablet
    #   InputDevice     "stylus"    "SendCoreEvents"
    #   InputDevice     "cursor"    "SendCoreEvents"
    #   InputDevice     "eraser"    "SendCoreEvents"
    Identifier  "Default Layout"
  screen 0 "Screen0" 0 0
    Inputdevice "Generic Keyboard"
    Inputdevice "Configured Mouse"
EndSection

Section "Files"
EndSection

Section "Module"
    Load        "glx"
EndSection

Section "ServerFlags"
    Option      "Xinerama"  "0"
EndSection

Section "InputDevice"
    Identifier  "Generic Keyboard"
    Driver      "kbd"
    Option      "CoreKeyboard"
    Option      "XkbRules"  "xorg"
    Option      "XkbModel"  "pc105"
    Option      "XkbLayout" "it"
EndSection

Section "InputDevice"
    Identifier  "Configured Mouse"
    Driver      "mouse"
    Option      "CorePointer"
    Option      "Device"    "/dev/input/mice"
    Option      "Protocol"  "ImPS/2"
    Option      "ZAxisMapping"  "4 5"
    Option      "Emulate3Buttons"   "true"
EndSection

Section "InputDevice"
    Identifier  "stylus"
    Driver      "wacom"
    Option      "Device"    "/dev/input/wacom"
    Option      "Type"  "stylus"
    Option      "ForceDevice"   "ISDV4"# Tablet PC ONLY
EndSection

Section "InputDevice"
    Identifier  "eraser"
    Driver      "wacom"
    Option      "Device"    "/dev/input/wacom"
    Option      "Type"  "eraser"
    Option      "ForceDevice"   "ISDV4"# Tablet PC ONLY
EndSection

Section "InputDevice"
    Identifier  "cursor"
    Driver      "wacom"
    Option      "Device"    "/dev/input/wacom"
    Option      "Type"  "cursor"
    Option      "ForceDevice"   "ISDV4"# Tablet PC ONLY
EndSection

Section "Monitor"
    Identifier  "Generic Monitor"
    Horizsync   30.0    -   70.0
    Vertrefresh 50.0    -   160.0
    Option      "DPMS"
EndSection

Section "Monitor"
    Identifier  "Monitor1"
    Vendorname  "Unknown"
    Modelname   "TV-0"
    Horizsync   28.0    -   33.0
    Vertrefresh 43.0    -   72.0
EndSection

Section "Monitor"
    Identifier  "Monitor0"
    Vendorname  "Unknown"
    Modelname   "Samsung SyncMaster"
    Horizsync   30.0    -   81.0
    Vertrefresh 56.0    -   75.0
EndSection

Section "Device"
    Identifier  "Generic Video Card"
    Driver      "nvidia"
    Option      "AddARGBVisuals"    "True"
    Option      "NoLogo"    "True"
EndSection

Section "Device"
    Identifier  "Videocard0"
    Driver      "nvidia"
    Vendorname  "NVIDIA Corporation"
    Boardname   "GeForce 7300 GT"
EndSection

Section "Device"
    Identifier  "Videocard1"
    Driver      "nvidia"
    Vendorname  "NVIDIA Corporation"
    Boardname   "GeForce 7300 GT"
    Busid       "PCI:1:0:0"
    Screen  1
EndSection

Section "Screen"
    Identifier  "Default Screen"
    Device      "Generic Video Card"
    Monitor     "Generic Monitor"
    Defaultdepth    24
    Option      "AddARGBVisuals"    "True"
    Option      "TripleBuffer"  "True"
    Option      "NoLogo"    "True"
    Option      "AddARGBGLXVisuals" "True"
    SubSection "Display"
        Depth   24
        Modes       "nvidia-auto-select"
    EndSubSection
EndSection

Section "Screen"
    Identifier  "Screen1"
    Device      "Videocard0"
    Monitor     "Monitor1"
    Defaultdepth    24
    Option      "TwinView"  "0"
    Option      "metamodes" "TV: 1024x768 +0+0"
    Option      "AddARGBGLXVisuals" "True"
    SubSection "Display"
        Depth   24
    EndSubSection
EndSection

Section "Screen"
    
    # Removed Option "metamodes" "CRT: nvidia-auto-select +0+0"
    # Removed Option "metamodes" "CRT: 1600x1200_60 +0+0; CRT: nvidia-auto-select +0+0"
    Identifier  "Screen0"
    Device      "Videocard0"
    Monitor     "Monitor0"
    Defaultdepth    24
    Option      "TwinView"  "0"
    Option      "metamodes" "1600x1200_60 +0+0; 1600x1200 +0+0"
    Option      "AddARGBGLXVisuals" "True"
    SubSection "Display"
        Depth   24
    EndSubSection
EndSection

Section "Extensions"
    Option      "Composite" "Enable"
EndSection
''', file=confFile)

        confFile.close()
        
        valid = True
        
        try:
            self.parser = xorgparser.Parser(tempFile)
        except ParseException:
            valid = False
        
        self.failUnless(valid == True, 'This file should be considered valid')

    def testIntegrity12(self):
        '''
        def get_identifier(self, section, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier  "pippo"
EndSection

Section "Screen"
    Identifier  "MGA 1"
EndSection

Section "Screen"
    Identifier  "MGA 3"
EndSection

Section "Screen"
    Identifier  "MGA 2"
    Device "pippo"
EndSection

Section "ServerLayout"
    Identifier  "Layout 1"
    Screen      "MGA 1"
    Screen      "MGA 2" RightOf "MGA 1"
    Screen      0 "MGA 3"
    InputDevice "Keyboard 1" "CoreKeyboard"
    InputDevice "Mouse 1"    "CorePointer"
    InputDevice "Mouse 2"    "SendCoreEvents"
    Option      "BlankTime"  "5"
EndSection
''', file=confFile)

        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity13(self):
        '''
        getDevicesInUse(self)
        
        case: More than 1 ServerLayout with ServerFlags with more than one default
           layout
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "bar"
EndSection

Section "Device"
    Identifier "Yet Another Video Device"
    Driver "bar"
EndSection

Section "Screen"
    Identifier "Default Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "New Screen Device"
    Device "Yet Another Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "A Layout"
    Option "Whatever"
    Screen "Default Screen Device" 0 0
    Screen "Another Screen Device" RightOf "Default Screen Device"
EndSection

Section "ServerLayout"
    Identifier "Another Layout"
    Option "Whatever"
    Screen "New Screen Device" 0 0
EndSection

Section "ServerFlags"
    Option "DefaultServerLayout" "A Layout"
EndSection

Section "ServerFlags"
    Option "DefaultServerLayout" "Another Layout"
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity14(self):
        '''
        getDevicesInUse(self)
        
        case: No ServerLayout and ServerFlags with one default
           layout
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "bar"
EndSection

Section "Device"
    Identifier "Yet Another Video Device"
    Driver "bar"
EndSection

Section "Screen"
    Identifier "Default Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "New Screen Device"
    Device "Yet Another Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerFlags"
    Option "DefaultServerLayout" "A Layout"
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity15(self):
        '''
        getDevicesInUse(self)
        
        case: One ServerLayout and ServerFlags with one default
              layout which doesn't exist
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "bar"
EndSection

Section "Device"
    Identifier "Yet Another Video Device"
    Driver "bar"
EndSection

Section "Screen"
    Identifier "Default Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "New Screen Device"
    Device "Yet Another Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "My layout"
    Screen "Another Screen Device"
EndSection

Section "ServerFlags"
    Option "DefaultServerLayout" "A Layout"
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)
    
    def testIntegrity16(self):
        '''
        getDevicesInUse(self)
        
        case: One ServerLayout and ServerFlags with one default
              layout which doesn't exist
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "bar"
EndSection

Section "Device"
    Identifier "Yet Another Video Device"
    Driver "bar"
EndSection

Section "Screen"
    Identifier "Default Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "New Screen Device"
    Device "Yet Another Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "My layout"
    Screen "Another Screen Device"
EndSection

Section "ServerFlags"
    Option "DefaultServerLayout" "A Layout"
    Enable
EndSection
''', file=confFile)
        confFile.close()
        
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def testIntegrity17(self):
        '''
        isDriverEnabled(self, driver)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Monitor"
    Identifier "Another Video Device"
    ModelName ""
EndSection
''', file=confFile)
        confFile.close()
        valid = True
        try:
            self.parser = xorgparser.Parser(tempFile)
        except ParseException:
            valid = False
         
        self.failUnless(valid == True, 'The xorg.conf should be valid!')

    def testIntegrity18(self):
        '''
        isDriverEnabled(self, driver)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Monitor"
    Identifier "Another Video Device"
    Enable
EndSection
''', file=confFile)
        confFile.close()
        self.assertRaises(ParseException,
                      xorgparser.Parser, tempFile)

    def test_get_position1(self):
        '''
        def get_position(self, section, identifier):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'XKit Screen'
        position1 = self.parser.make_section(section, identifier)
        position2 = self.parser.get_position(section, identifier)
        
        self.failUnless(position1 == position2, 
                        'The position was not correctly retrieved')

    def test_get_position2(self):
        '''
        def get_position(self, section, identifier):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier  "pippo"
EndSection

Section "Screen"
    Identifier  "MGA 1"
EndSection
''', file=confFile)
        confFile.close() 
        self.parser = xorgparser.Parser(tempFile)
        self.assertRaises(IdentifierException,
                      self.parser.get_position, 'Screen', 'Default')
    
    def test_write1(self):
        '''
        def write(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        x = self.parser = xorgparser.Parser()

        device = x.make_section('Device', identifier='Default Device')
        x.add_option('Device', 'Driver', 'mydrv', position=device)
        #x.setValue('Device', 'mydrv', device)

        oldDict = copy.deepcopy(x.globaldict)
        
        f = tempfile.TemporaryFile()
        
        x.write(f)

        newDict = x.globaldict
        self.assertEqual(oldDict, newDict)
    
    def test_write2(self):
        '''
        def write(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        x = self.parser = xorgparser.Parser()

        device = x.make_section('Device', identifier='Default Device')
        x.add_option('Device', 'Driver', 'mydrv', position=device)
        #x.setValue('Device', 'mydrv', device)

        oldDict = copy.deepcopy(x.globaldict)
        
        x.write(tempFile)

        newDict = x.globaldict
        self.assertEqual(oldDict, newDict)

    def test_write3(self):
        '''
        def write(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        x = self.parser = xorgparser.Parser()

        device = x.make_section('Device', identifier='Default Device')
        x.add_option('Device', 'Driver', 'mydrv', position=device)
        #x.setValue('Device', 'mydrv', device)

        oldDict = copy.deepcopy(x.globaldict)
        
        f = tempfile.TemporaryFile()
        x.write(f)

        self.assertEqual(oldDict, x.globaldict)

        f = tempfile.TemporaryFile()
        x.write(f)
        
        self.assertEqual(oldDict, x.globaldict)

    def test_write4(self):
        '''
        def write(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name

        fakeDeviceOption = '#Option Fake Setting'
        fakeMonitorOption = '#Option Fake ScreenSetting'
        inventedOption = '#this does not exist'

        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    #Option Fake Setting
    #another comment
EndSection

Section "Monitor"
    Identifier "Another Video Device"
EndSection

Section "Monitor"
    Identifier "Yet Another Video Device"
    #Option Fake ScreenSetting
EndSection
''', file=confFile)
        confFile.close()

        # Read the file
        y = self.parser = xorgparser.Parser(tempFile)
        # Remove the file
        os.remove(tempFile)
        # Write the data back
        y.write(tempFile)
        # Delete the object
        del y
        # Read what we wrote
        y = self.parser = xorgparser.Parser(tempFile)

        commentFound = False
        for commentSection in y.globaldict[y.commentsection]['Device']:
            if fakeDeviceOption in y.globaldict[y.commentsection]['Device'][commentSection]['options']:
                commentFound = True
                break

        self.assert_(commentFound)

        commentFound = False
        inventedFound = False
        for commentSection in y.globaldict[y.commentsection]['Monitor']:
            if fakeMonitorOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                commentFound = True
            if inventedOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                inventedFound = True

        self.assert_(commentFound)
        self.assert_(inventedFound == False)

    def testParseComments1(self):
        '''
        def __process(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        fakeDeviceOption = '#Option Fake Setting'
        fakeMonitorOption = '#Option Fake ScreenSetting'
        inventedOption = '#this does not exist'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    #Option Fake Setting
    #another comment
EndSection

Section "Monitor"
    Identifier "Another Video Device"
EndSection

Section "Monitor"
    Identifier "Yet Another Video Device"
    #Option Fake ScreenSetting
EndSection
''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        #print >> sys.stderr, str(y.globaldict)
        
        #y.write(sys.stderr)
        
        commentFound = False
        for commentSection in y.globaldict[y.commentsection]['Device']:
            if fakeDeviceOption in y.globaldict[y.commentsection]['Device'][commentSection]['options']:
                commentFound = True
                break
        
        self.assert_(commentFound)
        
        commentFound = False
        inventedFound = False
        for commentSection in y.globaldict[y.commentsection]['Monitor']:
            if fakeMonitorOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                commentFound = True
            if inventedOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                inventedFound = True
        
        self.assert_(commentFound)
        self.assert_(inventedFound == False)

    def testParseSubComments1(self):
        '''
        def __process(self, destination):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        fakeDeviceOption = '#Option Fake Setting'
        fakeMonitorOption = '#Option Fake ScreenSetting'
        inventedOption = '#this does not exist'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    #Option Fake Setting
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Monitor"
    Identifier "Another Video Device"
EndSection

Section "Monitor"
    Identifier "Yet Another Video Device"
    #Option Fake ScreenSetting
EndSection
''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        #print >> sys.stderr, str(y.globaldict)
        
        #y.write(sys.stderr)
        
        commentFound = False
        for commentSection in y.globaldict[y.commentsection]['Device']:
            if fakeDeviceOption in y.globaldict[y.commentsection]['Device'][commentSection]['options']:
                commentFound = True
                break
        
        self.assert_(commentFound)
        
        commentFound = False
        inventedFound = False
        for commentSection in y.globaldict[y.commentsection]['Monitor']:
            if fakeMonitorOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                commentFound = True
            if inventedOption in y.globaldict[y.commentsection]['Monitor'][commentSection]['options']:
                inventedFound = True
        
        self.assert_(commentFound)
        self.assert_(inventedFound == False)
        
        SubOption = '#I rock'
        commentFound = False
        for commentSection in y.globaldict[y.commentsection][y.subsection]:
            if SubOption in y.globaldict[y.commentsection][y.subsection][commentSection]['options']:
                commentFound = True
                break
        self.assert_(commentFound)
    
    
    def testCommentOutOption1(self):
        '''
        def commentOutOption(self, section, option, value=None, position=None, reference=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        option = 'Fake'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection
''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        #print >> sys.stderr, str(y.globaldict)
        
        #y.write(sys.stderr)
        
        
        found = False
        y.commentOutOption(section, option, value=None, position=None, reference=None)
        for position in y.globaldict[section]:
            lines = y.globaldict[section][position]
            for line in lines:
                if line.find(option) != -1:
                    found = True
                    #print line
            self.failUnless(found == False, 'Option not removed!')
        
        commentFound = False
        for commentSection in y.globaldict[y.commentsection]['Device']:
            if '#Option Fake True' in y.globaldict[y.commentsection]['Device'][commentSection]['options']:
                commentFound = True
                break
        
        #print >> sys.stderr, str(y.globaldict)
        
        self.assert_(commentFound)
        #y.write(sys.stderr)
    
    def testCommentOutSubOption1(self):
        '''
        def commentOutSubOption(self, section, identifier, option, position=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        y.commentOutSubOption(section, identifier, option, position=None)
        
        commentFound = False
        for commentSection in y.globaldict[y.commentsection][y.subsection]:
            if y.globaldict[y.commentsection][y.subsection][commentSection]['section'] == 'Screen':
                if '#Depth 24' in y.globaldict[y.commentsection][y.subsection][commentSection]['options']:
                    commentFound = True
                    break
        
        
        for pos in self.parser.globaldict['SubSection']:
            subsection = self.parser.globaldict['SubSection'][pos]
            if subsection.get('identifier') == identifier and \
            subsection.get('section') == section:
                lines = subsection.get('options')
                found = False
                for line in lines:
                    if line.find(option) != -1:
                        found = True
                self.failUnless(found == False, 'Option not commented out from all the Subsections')
        
        
#        print >> sys.stderr, str(y.globaldict)
#        y.write(sys.stderr)
        self.assert_(commentFound)

    def test_get_subsections1(self):
        '''def get_subsections(self, section, position)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection


''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(len(screenSub0) == 1)
        
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(len(screenSub1) == 2)
        
    def test_comment_out_section1(self):
        '''1 def comment_out_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen1"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        # the screen sections should have a 
        # reference to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        
        # Comment out the first Screen section
        y.comment_out_section('Screen', identifier='My Screen')
        
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen was commented out together with
        # its subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(not screenSub0)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(len(screenSub1) == 2)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(not y.globaldict['Screen'].get(0))
        
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
                #print >> sys.stderr, "\n\nfound 0 in", str(elem)
            elif elem[1] == 1:
                hasIdentifier1 = True
                #print >> sys.stderr, "\n\nfound 1 in", str(elem)
        
        
        
        self.assert_(not hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        
        # Comment out the 2nd Screen section
        y.comment_out_section('Screen', identifier='My Screen1')
        self.assert_(not y.globaldict['Screen'].get(1))
        
        # the second Screen was commented out together with
        # its subsection
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
                #print >> sys.stderr, "\n\nfound 0 in", str(elem)
            elif elem[1] == 1:
                hasIdentifier1 = True
                #print >> sys.stderr, "\n\nfound 1 in", str(elem)
        
        
        self.assert_(not hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)

    def test_comment_out_section2(self):
        '''2 def comment_out_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen1"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = self.parser = xorgparser.Parser(tempFile)
        
        # the screen sections should have a 
        # reference to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        
        # Comment out the first Screen section
        y.comment_out_section('Screen', position=0)
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
                #print >> sys.stderr, "\n\nfound 0 in", str(elem)
            elif elem[1] == 1:
                hasIdentifier1 = True
                #print >> sys.stderr, "\n\nfound 1 in", str(elem)
        
        
        self.assert_(not hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen was commented out together with
        # its subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(not screenSub0)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(len(screenSub1) == 2)
        
        
        self.assert_(not y.globaldict['Screen'].get(0))
        
        # Comment out the 2nd Screen section
        y.comment_out_section('Screen', position=1)
        self.assert_(not y.globaldict['Screen'].get(1))
        
        # the second Screen was commented out together with
        # its subsection
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
        
        # check that the removed sections don't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
                #print >> sys.stderr, "\n\nfound 0 in", str(elem)
            elif elem[1] == 1:
                hasIdentifier1 = True
                #print >> sys.stderr, "\n\nfound 1 in", str(elem)
        
        
        self.assert_(not hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        
        #y.write(sys.stderr)
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)

    def test_comment_out_section3(self):
        '''3 def comment_out_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen1"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
#        print >> sys.stderr, str(y.globaldict)

        # screen sections should have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)


        # Comment out the all Screen sections
        y.comment_out_section('Screen')
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen was commented out together with
        # its subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(not screenSub0)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(not y.globaldict['Screen'].get(0))
        
        self.assert_(not y.globaldict['Screen'].get(1))
        
        
        # the screen sections should not have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(not hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        #y.write(sys.stderr)
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)

    def test_comment_out_section4(self):
        '''4 def comment_out_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "ServerFlags"
    Option "IgnoreAbi" "True"
EndSection

#Section "Screen"
#    Identifier "My Screen1"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
        
#        print >> sys.stderr, str(y.globaldict)
#        print >> sys.stderr, '\n'

        # the screen sections should have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)


        # Comment out the first Screen section
        y.comment_out_section('Screen', position=0)
        
#        print >> sys.stderr, str(y.globaldict)
#        print >> sys.stderr, '\n'
        
        
        # screen 0 should not have a reference to
        # its id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(not hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen was commented out together with
        # its subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(not screenSub0)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(len(screenSub1) == 2)
        
        
        self.assert_(not y.globaldict['Screen'].get(0))
        
        # Comment out the 2nd Screen section
        y.comment_out_section('Screen', position=1)
        self.assert_(not y.globaldict['Screen'].get(1))
        
        # the second Screen was commented out together with
        # its subsection
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
        # screens should not have a reference to their id
        # in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(not hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        
        
        # ServerFlags should exist
        self.assert_(y.globaldict['ServerFlags'].get(0))
        
        # serverFlags should not have a reference to its id
        # in y.identifiers
        self.assert_(not y.identifiers.get('ServerFlags'))
                
        
        # comment out ServerFlags
        y.comment_out_section('ServerFlags')
        # ServerFlags should not exist
        self.assert_(not y.globaldict['ServerFlags'].get(0))
        
        # Make sure that the option in ServerFlags was preserved
        # in the comments
        commentFound = False
        for line in y.comments:
            if line.find('Option "IgnoreAbi" "True"') != -1:
                commentFound = True
                break
        
        # serverFlags should not have a reference to its id
        # in y.identifiers
        self.assert_(not y.identifiers.get('ServerFlags'))
                
        self.assert_(commentFound)
        
        #y.write(sys.stderr)
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)



    def testCommentOutSubSection(self):
        '''def commentOutSubSection(self, section, identifier, position=None):'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen3"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
#        print >> sys.stderr, str(y.globaldict)
        # Try to comment out a subsection which doesn't exist
        y.commentOutSubSection('Screen', 'Whatever', 0)
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen has 1 subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(len(screenSub0) == 1)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(len(screenSub1) == 2)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(y.globaldict['Screen'].get(1))
        
        # Remove "Whatever" subsection from Screen 1
        y.commentOutSubSection('Screen', 'Whatever', 1)
        
        screenSub1 = y.get_subsections('Screen', 1)
        # Screen 1 must have only 1 subsection now
        self.assert_(len(screenSub1) == 1)
        
        # Make sure that the Screen sections are still there
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(y.globaldict['Screen'].get(1))
        
        # Let's assume that I change my mind at this point and
        # decide to comment out the whole section
        y.comment_out_section('Screen', position=1)
        self.assert_(not y.globaldict['Screen'].get(1))
        
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)
        #y.write(sys.stderr)

    def test_remove_section1(self):
        '''by identifier def remove_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen3"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(y.globaldict['Screen'].get(1))
#        print >> sys.stderr, str(y.globaldict)
        
        # the screen sections should have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        # Remove Screen "My Screen 1"
        y.remove_section('Screen', identifier='My Screen1')
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen has 1 subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(len(screenSub0) == 1)
        
        # Screen section 2 has 2 subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(not y.globaldict['Screen'].get(1))
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(not hasIdentifier1)
                
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)
        #y.write(sys.stderr)
        
        
    def test_remove_section2(self):
        '''by position def remove_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen3"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(y.globaldict['Screen'].get(1))
#        print >> sys.stderr, str(y.globaldict)
        
        # the screen sections should have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        # Remove Screen section 1
        y.remove_section('Screen', position=1)
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen has 1 subsection
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(len(screenSub0) == 1)
        
        # Screen section 2 has no subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(not y.globaldict['Screen'].get(1))
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)
        #y.write(sys.stderr)
    
    def test_remove_section3(self):
        '''by type def remove_section(self, section, identifier=None, position=None)'''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Screen'
        identifier = 'Display'
        option = 'Depth'
        
        confFile = open(tempFile, 'w')
        print('''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
    Option Fake True
    #another comment
EndSection

Section "Screen"
    Identifier "My Screen"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
EndSection

Section "Screen"
    Identifier "My Screen1"
    Subsection "Display"
        Depth 24
        #I rock
    EndSubSection
    Subsection "Whatever"
        Depth 24
        #I rock
    EndSubSection
EndSection

#Section "Screen"
#    Identifier "My Screen3"
#    Subsection "Display"
#        Depth 24
#        #I rock
#    EndSubSection
#    Subsection "Whatever"
#        Depth 24
#        #I rock
#    EndSubSection
#EndSection


''', file=confFile)
        confFile.close()
        
        y = xorgparser.Parser(tempFile)
        
        self.assert_(y.globaldict['Screen'].get(0))
        
        self.assert_(y.globaldict['Screen'].get(1))
        
        self.assert_(y.globaldict['Device'].get(0))
#        print >> sys.stderr, str(y.globaldict)
        
        # the screen sections should have a reference
        # to their id in y.identifiers
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
            elif elem[1] == 1:
                hasIdentifier1 = True
        
        self.assert_(hasIdentifier0)
        self.assert_(hasIdentifier1)
        
        # Remove any Screen section
        y.remove_section('Screen')
        
        # the Device section doesn't have subsections
        deviceSub = y.get_subsections('Device', 0)
        self.assert_(not deviceSub)
        
        # the first Screen has no subsections
        screenSub0 = y.get_subsections('Screen', 0)
        self.assert_(not screenSub0)
        
        # Screen section 2 has no subsections
        screenSub1 = y.get_subsections('Screen', 1)
        self.assert_(not screenSub1)
        
#        print >> sys.stderr, str(y.globaldict)
        
        self.assert_(not y.globaldict['Screen'].get(0))
        
        self.assert_(not y.globaldict['Screen'].get(1))
        
        self.assert_(y.globaldict['Device'].get(0))
        
        # check that the removed section doesn't have
        # a reference in y.identifiers any longer
        hasIdentifier0 = False
        hasIdentifier1 = False
        for elem in y.identifiers['Screen']:
            if elem[1] == 0:
                hasIdentifier0 = True
                #print >> sys.stderr, "\n\nfound 0 in", str(elem)
            elif elem[1] == 1:
                hasIdentifier1 = True
                #print >> sys.stderr, "\n\nfound 1 in", str(elem)
        
        
        self.assert_(not hasIdentifier0)
        self.assert_(not hasIdentifier1)
        
        y.write(tempFile)
        
        # Make sure that the output validates
        y = self.parser = xorgparser.Parser(tempFile)
        #y.write(sys.stderr)
    
    def testOptionPrefix(self):
        '''Make sure that the option has quotation marks when required'''
        self.this_function_name = sys._getframe().f_code.co_name
        y = xorgparser.Parser()
        
        section = 'ServerFlags'
        
        y.add_option(section, 'OffTime', 1, option_type='Option', prefix='')
        self.assert_(y.globaldict[section][0][0] == '\tOption\t"OffTime"\t1\n')

        y.add_option(section, 'OffTime', 1, option_type='Option', prefix='"')
        self.assert_(y.globaldict[section][0][0] == '\tOption\t"OffTime"\t"1"\n')
        
        y.add_option(section, 'OffTime', 1, option_type=None, prefix='')
        self.assert_(y.globaldict[section][0][0] == '\tOffTime\t1\n')
        
        y.add_option(section, 'OffTime', 1)
        self.assert_(y.globaldict[section][0][0] == '\tOffTime\t"1"\n')

    
if __name__ == '__main__':
    a = open(destinationFile, 'w')
    a.write('')
    a.close()
    unittest.main()
