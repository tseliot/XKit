#       1-test.py -- Test suite for xutils
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

from XKit import xutils
from XKit.xutils import *
import sys
import unittest
import os
import settings

source = settings.inputFile
destination = settings.outputDir
destinationFile = os.path.join(settings.outputDir, 'xkittest-1.txt')
tempFile = os.path.join(destination, 'tmp')

section = 'Device'

class XUtilsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.parser = xutils.XUtils(source)
    
    def tearDown(self):
        self.parser.comments.insert(0, '\n-----' + self.this_function_name + '-----\n')
        self.parser.writeFile(destinationFile, test=True)
        try:
            os.remove(tempFile)
        except(OSError, IOError):
            pass
    
    def testCheckNFixSection1(self):
        '''
        def checkNFixSection(self, section, position=None, identifier=None):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        '''
        Section "Screen"
            Identifier "Default Screen Device"
            Device "Yet Another Video Device"
        EndSection

        Section "Screen"
            Identifier "Another Screen Device"
            Device "Another Video Device"
        EndSection

        Section "ServerLayout"
            Identifier "A Layout"
            InputDevice "Mouse 1"
            Screen "Screen1" 0 0
        EndSection
        '''
        
        self.parser = xutils.XUtils(None)
        
        screen1 = self.parser.makeSection('Screen', identifier='Default Screen Device')
        self.parser.addReference('Screen', 'Device', 'Yet Another Video Device', position=screen1)
        
        screen2 = self.parser.makeSection('Screen', identifier='Another Screen Device')
        self.parser.addReference('Screen', 'Device', 'Another Video Device', position=screen2)
        
        layout = self.parser.makeSection('ServerLayout', identifier='A Layout')
        
        self.parser.addReference('ServerLayout', 'Screen', 'Screen1', position=layout)
        
        self.parser.addReference('ServerLayout', 'InputDevice', 'Mouse 1', position=layout)
        
        self.parser.checkNFixSection()
        
        
        screens = len(self.parser.globaldict['Screen'])
        devices = len(self.parser.globaldict['Device'])
        inputDevices = len(self.parser.globaldict['InputDevice'])
        
        expectedScreens = 3
        expectedDevices = 2
        expectedInputDevices = 1
        
        self.failUnless(screens == expectedScreens and devices == expectedDevices and inputDevices == expectedInputDevices, 'Not all the broken sections were fixed!')
    
    def testGetDriver(self):
        '''
        def getDriver(self, section, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Video Device'
        option = 'Driver'
        driver1 = 'xkit'
        position = self.parser.makeSection(section, identifier=identifier)
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
        
        self.parser.addOption(section, option, driver1, position=position)
        
        driver2 = self.parser.getDriver(section, position)
        
        self.failUnless(driver1 == driver2, 'Driver not correctly retrieved!')
    
    def testSetDriver(self):
        '''
        def setDriver(self, section, driver, position):
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Video Device'
        option = 'Driver'
        driver = 'xkit'
        position = self.parser.makeSection(section, identifier=identifier)
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
        
        self.parser.addOption(section, option, driver, position=position)
        
        driver1 = self.parser.getDriver(section, position)
        
        self.setUp()
        
        position = self.parser.makeSection(section, identifier=identifier)
        sect = self.parser.globaldict[section].get(position)
        self.failUnless(sect != None, 'Section not created!')
        
        self.parser.setDriver(section, driver, position)
        driver2 = self.parser.getDriver(section, position)
        
        self.failUnless(driver1 == driver2, 'Driver not correctly set!')

    def testIsDriverInSection(self):
        '''
        isDriverInSection(self, driver, sectionsList=None)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        section = 'Device'
        identifier = 'XKit Video Device'
        option = 'Driver'
        driver = 'xkit'
        
        self.parser = xutils.XUtils()
        
        position = self.parser.makeSection(section, identifier=identifier)
        self.parser.addOption(section, option, driver, position=position)
        
        status = self.parser.isDriverInSection(driver, sectionsList=[position])
        
        self.failUnless(status == True, 'Driver not in section!')

    def testGetDevicesFromServerLayout1(self):
        '''
        getDevicesFromServerLayout(self, position)
        
        case: no references
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Device "Yet Another Video Device"
EndSection

Section "Device"
    Identifier "Another Screen Device"
    Device "Default Video Device"
EndSection

Section "Device"
    Identifier "Yet Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "A Layout"
    Screen "Default Screen Device"
    Option "Whatever"
EndSection
'''
        confFile.close()
        
        self.parser = xutils.XUtils(tempFile)
        devices = self.parser.getDevicesFromServerLayout(0)
        
        self.failUnless(len(devices) == 1, 'Only one section should be found!')
    
    def testGetDevicesFromServerLayout2(self):
        '''
        getDevicesFromServerLayout(self, position)
        
        case: good references (the sections referred to in the layout exist)
        
        A typical Xinerama setup
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Device "Yet Another Video Device"
EndSection

Section "Device"
    Identifier "Another Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "Device"
    Identifier "Yet Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "A Layout"
    Option "Whatever"
    Screen "Default Screen Device" 0 0
    Screen "Another Screen Device" RightOf "Default Screen Device"
EndSection
'''
        confFile.close()
        
        self.parser = xutils.XUtils(tempFile)
        devices = self.parser.getDevicesFromServerLayout(0)
        
        self.failUnless(len(devices) == 2, 'No section should be found!')
    
    
    def testGetDevicesInUse1(self):
        '''
        getDevicesInUse(self)
        
        case: No ServerLayout
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Device "Yet Another Video Device"
EndSection

Section "Device"
    Identifier "Another Screen Device"
    Device "Default Video Device"
EndSection

Section "Device"
    Identifier "Yet Another Screen Device"
    Device "Another Video Device"
EndSection

'''
        confFile.close()

        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        devices.sort()
        
        self.failUnless(devices == self.parser.globaldict['Device'].keys(), 'All the Device sections should be returned!')

    def testGetDevicesInUse2(self):
        '''
        getDevicesInUse(self)
        
        case: 1 ServerLayout with no references to Screen sections
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Device "Yet Another Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "Yet Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "Layout 1"
    Screen "Yet Another Screen Device" LeftOf "Another Screen Device"
    Screen "Another Screen Device"
EndSection
'''
        confFile.close()
        
        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        devices.sort()
        
        self.failUnless(len(devices) == 2, 'Only 2 Device sections should have been returned!')

    def testGetDevicesInUse3(self):
        '''
        getDevicesInUse(self)
        
        case: 1 ServerLayout with references to Screen sections
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Device "Yet Another Video Device"
EndSection

Section "Device"
    Identifier "Another Screen Device"
    Device "Default Video Device"
EndSection

Section "Screen"
    Identifier "Another Screen Device"
    Device "Another Video Device"
EndSection

Section "Device"
    Identifier "Yet Another Screen Device"
    Device "Another Video Device"
EndSection

Section "ServerLayout"
    Identifier "A Layout"
    Option "Whatever"
    Screen "Default Screen Device" 0 0
    Screen "Another Screen Device" RightOf "Default Screen Device"
EndSection
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        
        self.failUnless(len(devices) == 2, 'Only 2 Device sections should be found!')
        
    def testGetDevicesInUse4(self):
        '''
        getDevicesInUse(self)
        
        case: More than 1 ServerLayout with no ServerFlags
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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

'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        
        self.failUnless(len(devices) == 3, 'Only 3 Device sections should be found!')

    def testGetDevicesInUse5(self):
        '''
        getDevicesInUse(self)
        
        case: More than 1 ServerLayout with ServerFlags with no default layout
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
    Option "Whatever"
EndSection
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        self.failUnless(len(devices) == 3, 'Only 3 Device sections should be found!')

    def testGetDevicesInUse6(self):
        '''
        getDevicesInUse(self)
        
        case: More than 1 ServerLayout with ServerFlags with one default layout
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        
        devices = self.parser.getDevicesInUse()
        
        self.failUnless(len(devices) == 2, 'Only 2 Device sections should be found!')

    def testIsDriverEnabled1(self):
        '''
        isDriverEnabled1(self, driver)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        enabled = self.parser.isDriverEnabled('foo')
        
        self.failUnless(enabled == False, 'The driver should not be enabled!')
        
        enabled = self.parser.isDriverEnabled('bar')
        self.failUnless(enabled == False, 'The driver should not be enabled!')
        
    def testIsDriverEnabled2(self):
        '''
        isDriverEnabled2(self, driver)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "bar"
EndSection
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        enabled = self.parser.isDriverEnabled('foo')
        
        self.failUnless(enabled == False, 'The driver should not be enabled!')
        
        enabled = self.parser.isDriverEnabled('bar')
        self.failUnless(enabled == False, 'The driver should not be enabled!')

    def testIsDriverEnabled3(self):
        '''
        isDriverEnabled3(self, driver)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
Section "Device"
    Identifier "Default Video Device"
    Driver "foo"
EndSection

Section "Device"
    Identifier "Another Video Device"
    Driver "foo"
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
'''
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        enabled = self.parser.isDriverEnabled('foo')
        
        self.failUnless(enabled == True, 'The driver should be enabled!')
        
        enabled = self.parser.isDriverEnabled('bar')
        self.failUnless(enabled == False, 'The driver should not be enabled!')

    def testGetScreenDeviceRelationships(self):
        '''
        getScreenDeviceRelationships(self)
        '''
        self.this_function_name = sys._getframe().f_code.co_name
        
        confFile = open(tempFile, 'w')
        print >> confFile, '''
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
'''        
        confFile.close()
        self.parser = xutils.XUtils(tempFile)
        relationships = self.parser.getScreenDeviceRelationships()
        
        correct = {0: {'Screen': 0}, 1: {'Screen': 2}, 2: {'Screen': 1}}
        
        relationsNumber = len(correct)
        
        trustRelationships = True
        if len(relationships) == relationsNumber:
            for relation in relationships:
                if relationships[relation] != correct[relation]:
                    trustRelationships = False
        else:
            trustRelationships = False
        
        self.failUnless(trustRelationships == True, 'Relationships do NOT match!')

if __name__ == '__main__':
    a = open(destinationFile, 'w')
    a.write('')
    a.close()    
    unittest.main()
