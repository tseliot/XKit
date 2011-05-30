#       0-example.py -- Examples which rely on xorgparser
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
import os

def main():
    '''
    Replace the first line of this example with a source and a destination file
    '''
    destination = os.path.join(os.path.expanduser('~'), 'xorgnew.txt')
    #source = '/etc/X11/xorg.conf'
    source = None
    a = Parser(source)
    
    '''
    Remove the Defaultdepth from all the Screen sections
    '''
    a.removeOption('Screen', 'DefaultDepth')
    
    '''
    Remove the Defaultdepth from the 1st Screen section
    '''
    a.removeOption('Screen', 'DefaultDepth', position=0)
    
    '''
    Set the Defaultdepth to 24 bit in all sections
    '''
    a.add_option('Screen', 'Defaultdepth', '24')
    '''
    Set the Defaultdepth to 24 bit in the 1st Screen section
    '''
    a.add_option('Screen', 'Defaultdepth', '24', position=0, prefix='')
    
    '''
    Get the value assigned to the AddARGBGLXVisuals option in the 1st Screen section
    '''
    try:
        print('AddARGBGLXVisuals', a.getValue('Screen', 'AddARGBGLXVisuals', position=1, identifier='Display'))
    except OptionException as e:
        print('Error:', e)
    
    '''
    Add an Option (with the Option prefix) to the 1st Screen section
    '''
    a.add_option('Screen', 'AddARGBGLXVisuals', 'True', option_type='Option', position=0)
    
    '''
    Print the global dict i.e. the dict which contains all sections
    '''
    print('\nGlobal dict is the dict which contains all sections\n', a.globaldict)
    #print '\nGlobal iters is\n', a.globaliters
    
    '''
    Make a new Device and a Screen section with an identifier
    '''
    a.makeSection('Device', identifier='Name of this new Device Section')
    a.makeSection('Screen', identifier='Default Screen')
    
    '''
    Add a reference to the Screen section identified as "New Default Screen" to
    the 1st ServerLayout section
    '''
    print('\nNew Default Screen in progress')
    a.addReference('ServerLayout', 'Screen', 'New Default Screen', position=0)
    a.addReference('ServerLayout', 'InputDevice', 'New Device', position=0)
    a.removeReference('ServerLayout', 'InputDevice', 'New Device', position=0)
    '''
    Add a reference to the Screen section identified as "New Default Screen" to
    all the ServerLayout sections
    '''
    #a.addReference('ServerLayout', 'Screen', 'New Default Screen', position=0)
    
    '''
    Remove a reference to the Screen section identified as "New Default Screen"
    from all the ServerLayout sections
    '''
    #a.removeReference('ServerLayout', 'Screen', 'New Default Screen')#, position=0)
    
    '''
    Create a new "Display" SubSection inside all the Screen sections
    '''
    a.makeSubSection('Screen', 'Display')#, position=0)
    '''
    Remove a "Display" SubSection inside all the Screen sections
    '''
    #a.removeSubSection('Screen', 'Display')#, position=0)
    
    '''
    Add an option to the Display subsection of the 1st Screen section
    '''
    a.addSubOption('Screen', 'Display', 'Depth', value='24', position=0)
    a.addSubOption('Screen', 'Display', 'Virtual', value='1600 1200', position=0)
    a.addSubOption('Screen', 'Display', 'Name', value='Whatever', option_type='Option', position=None)
    
    '''
    Remove options from the Display subsection of all or of the 1st Screen section
    '''
    a.removeSubOption('Screen', 'Display', 'Depth')
    a.removeSubOption('Screen', 'Martin', 'Virtual', position=0)
    
    
    '''
    Get the identifier of the 1st Device section
    '''
    print(a.getValue('Device', 'Identifier', 0))
    #print a.getValue('SubSection', 'Name', position=0, identifier='Display', sect='Screen')
    
    
    a.makeSection('Screen', 'New Screen')
    a.makeSection('Screen', 'New Screen')#this new section won't be created
    
    '''
    Create a new device section
    add a new option to it
    and make a reference to it in the Screen section
    '''
    dev = a.makeSection('Device', 'My Device')
    a.add_option('Device', 'BusID', 'PCI:1:0:0', position=dev)
    a.addReference('Screen', 'Device', 'My Device', position=0)
    
    a.addReference('Device', 'Screen', 4, position=0)
    print(a.getReferences('Screen', 0, reflist=['Device']))
    
    print('Virtual', a.getValue('SubSection', 'Virtual', position=0, identifier='Display', sect='Screen'))
    print('Modes', a.getValue('SubSection', 'Modes', position=0, identifier='Display', sect='Screen'))
    
    '''
    Create a new Device section and print the list of identifiers so as to see
    that the new identifier and position are included in identifiers
    '''
    a.makeSection('Device', identifier='New Graphics Card')
    
    print('\nCreate Broken Screen section')
    pos = a.makeSection('Screen', identifier='Broken Screen Section')
    print('\nAdding References')
    a.addReference('Screen', 'Monitor', 'Broken Monitor Section', position=pos)
    a.addReference('Screen', 'Device', 'Broken Device Section', position=pos)
    
    try:
        print('Horizsync value is', a.getValue('Monitor', 'Horizsync', 0))
    except OptionException as e:
        print('Error:', e)
    
    '''
    Write the changes to the destination file
    '''
    a.writeFile(destination)

if __name__ == '__main__': main()
