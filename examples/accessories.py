#       accessories.py -- Accessory class for commonly used options
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

from xkit import xutils
from xkit.xutils import *

class Accessories(XUtils):
    def __init__(self, source=None):
        XUtils.__init__(self, source)
    
    def printReferences(self):
        self.referencesTree = {}
        for section in ['Screen', 'ServerLayout']:
            self.referencesTree[section] = {}
            for sect in self.globaldict[section]:
                self.referencesTree[section][sect] = self.getReferences(section, sect)
                print(sect, 'Section - references:', self.getReferences(section, sect))
        for section in self.referencesTree:
            for elem in self.referencesTree[section]:
                #print 'ELEMENT', elem
                for refsect in self.referencesTree[section][elem]:
                    if len(self.referencesTree[section][elem][refsect]) > 0:
                        print('\n', section, 'Section', '"' + self.getIdentifier(section, elem) + '"', 'depends on', \
                        'Section', refsect, ':\n', \
                        self.referencesTree[section][elem][refsect])
                        for ref in self.referencesTree[section][elem][refsect]:
                            for sect in self.sections:
                                if sect.lower() == refsect.strip().lower():
                                    refsect = sect
                            if not self.isSection(refsect, ref):
                                print('*****WARNING:', refsect, 'Section', ref, 'does not exist!*****')
    
    def printDuplicateOptions(self):
        '''
        Print the duplicate options
        '''
        a = self.check_duplicate_options()
        if len(a) > 0:
            print('\nDuplicate Options:')
            for section in a:
                print('Duplicate Options in', section, 'Section:')
                for elem in a[section]:
                    print('\tSection No:', elem)
                    for option in a[section][elem]:
                        print('\t\t', option)
        else:
            print('No Duplicate Options Found')
    
    def printDuplicateSections(self):
        a = self.getDuplicateSections()
        print('\nDuplicate Sections:')
        for section in a:
            print('Duplicate', section, 'Sections:')
            for elem in a[section]:
                print('\t', elem)    
    
    def printSection(self, section):
        '''
        Print the content of all the sections of a certain type
        '''
        for elem in self.globaldict[section]:
            print('Section' + '"' + section + '"')
            print(''.join(self.globaldict[section][elem]) + 'EndSection\n')
    
    def getDefaultDepth(self, position):
        '''
        Get the Defaultdepth in an instance of the Screen section. If none is
        found, return False.
        
        For further information see getValue
        '''
        option = 'DefaultDepth'
        section = 'Screen'
        return self.getValue(section, option, position)
        
    def setDefaultDepth(self, depth, position):
        '''
        Set the Defaultdepth in an instance of the Screen section.
        '''
        section = 'Screen'
        option = 'DefaultDepth'
        self.add_option(section, option, depth, position=position, prefix='')
    
    '''
    It would make a lot sense to move the following methods to another file
    '''
    
    def addArgbGlxVisuals(self, position):
        section = 'Screen'
        option = 'AddARGBGLXVisuals'
        self.add_option(section, option, 'True', option_type='Option', position=position)

    def removeArgbGlxVisuals(self, position):
        section = 'Screen'
        option = 'AddARGBGLXVisuals'
        self.add_option(section, option, position=position)
        
    def enableComposite(self, position=0):
        section = 'Extensions'
        option = 'Composite'
        if len(self.globaldict[section]) == 0:
            position = self.makeSection(section)
        self.add_option(section, option, 'Enable', option_type='Option', position=position)
        
    def disableComposite(self, position=0):
        section = 'Extensions'
        option = 'Composite'
        if len(self.globaldict[section]) == 0:
            position = self.makeSection(section)
        self.add_option(section, option, 'Disable', option_type='Option', position=position)
