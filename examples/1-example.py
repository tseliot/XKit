#       1-example.py -- Examples which rely on accessories 
#                       (and therefore also on xutils)
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

from .accessories import *
import os

def main():
    '''
    Replace the first line of this example with a source and a destination file
    '''
    destination = os.path.join(os.path.expanduser('~'), 'xorgnew.txt')
    source = None
    a = Accessories(source)
    
    '''
    Remove the Defaultdepth from all the Screen sections
    '''
    a.remove_option('Screen', 'DefaultDepth')
    
    '''
    Remove the Defaultdepth from the 1st Screen section
    '''
    a.remove_option('Screen', 'DefaultDepth', position=0)
    
    '''
    Set the Defaultdepth to 24 bit in all sections
    '''
    a.add_option('Screen', 'Defaultdepth', '24', prefix='')
    '''
    Set the Defaultdepth to 24 bit in the 1st Screen section
    '''
    a.add_option('Screen', 'Defaultdepth', '24', position=0, prefix='')
    
    '''
    Get the value assigned to the AddARGBGLXVisuals option in the 1st Screen section
    '''
    try:
        print('AddARGBGLXVisuals', a.get_value('Screen', 'AddARGBGLXVisuals', position=1, identifier='Display'))
    except OptionNotAvailableException as e:
        print('Error:', e)
    '''
    Add an Option (with the Option prefix) to the 1st Screen section
    '''
    a.add_option('Screen', 'AddARGBGLXVisuals', 'True', option_type='Option', position=0)
    
    '''
    Print the contents of all the Device sections
    '''
    a.printSection('Device')
    
    '''
    Print the global dict i.e. the dict which contains all sections
    '''
    print('\nGlobal dict is the dict which contains all sections\n', a.globaldict)
    #print '\nGlobal iters is\n', a.globaliters
    
    '''
    Make a new Device and a Screen section with an identifier
    '''
    a.make_section('Device', identifier='Name of this new Device Section')
    a.make_section('Screen', identifier='Default Screen')
    
    '''
    Add a reference to the Screen section identified as "New Default Screen" to
    the 1st ServerLayout section
    '''
    a.add_reference('ServerLayout', 'Screen', 'New Default Screen')
    '''
    Add a reference to the Screen section identified as "New Default Screen" to
    all the ServerLayout sections
    '''
    a.add_reference('ServerLayout', 'Screen', 'New Default Screen', position=0)
    
    '''
    Remove a reference to the Screen section identified as "New Default Screen"
    from all the ServerLayout sections
    '''
    a.remove_reference('ServerLayout', 'Screen', 'New Default Screen')#, position=0)
    
    '''
    Create a new "Display" SubSection inside all the Screen sections
    '''
    a.make_subsection('Screen', 'Display')#, position=0)
    '''
    Remove a "Display" SubSection inside all the Screen sections
    '''
    #a.remove_subsection('Screen', 'Display')#, position=0)
    
    '''
    Add an option to the Display subsection of the 1st Screen section
    '''
    a.add_suboption('Screen', 'Display', 'Depth', value='24', position=0, prefix='')
    a.add_suboption('Screen', 'Display', 'Virtual', value='1600 1200', position=0)
    a.add_suboption('Screen', 'Display', 'Name', value='Whatever', option_type='Option', position=None)
    
    '''
    Remove options from the Display subsection of all or of the 1st Screen section
    '''
    a.remove_suboption('Screen', 'Display', 'Depth')
    a.remove_suboption('Screen', 'Martin', 'Virtual', position=0)
    
    
    '''
    Get the identifier of the 1st Device section
    '''
    print(a.get_value('Device', 'Identifier', 0))
    #print a.get_value('SubSection', 'Name', position=0, identifier='Display', sect='Screen')
    
    
    '''
    Set the driver  of the 1st Device section
    '''
    a.setDriver('Device', 'fbdev', 0)
    '''
    Get the driver  of the 1st Device section
    '''
    print(a.getDriver('Device', 0))
    
    
    a.make_section('Screen', 'New Screen')
    a.make_section('Screen', 'New Screen')#this new section won't be created
    a.setDefaultDepth(24, 0)
    print(a.getDefaultDepth(0))
    
    '''
    Create a new device section
    add a new option to it
    and make a reference to it in the Screen section
    '''
    dev = a.make_section('Device', 'My Device')
    a.add_option('Device', 'BusID', 'PCI:1:0:0', position=dev)
    a.add_reference('Screen', 'Device', 'My Device', position=0)
    
    a.add_reference('Device', 'Screen', 4, position=0)
    print(a.get_references('Screen', 0, reflist=['Device']))
    a.enableComposite()
    a.addArgbGlxVisuals(0)
    
    print('Virtual', a.get_value('SubSection', 'Virtual', position=0, identifier='Display', sect='Screen'))
    print('Modes', a.get_value('SubSection', 'Modes', position=0, identifier='Display', sect='Screen'))
    
    '''
    Get the identifier of the first Device section
    '''
    print('ID of the 1st Device Section =', a.get_identifier('Device', 0))
    
    '''
    Get the position of the Device section identified as 'Configured Video Device'
    '''
    try:
        print('Position of "Configured Video Device" =', a.getPosition('Device', 'Configured Video Device'))
    except IdentifierException as e:
        print(e)
    '''
    See if a section exists
    '''
    print('Section Device "Configured Video Device" exists =', a.isSection('Device', 'Configured Video Device'))
    print('Section Device "Whatever" exists =', a.isSection('Device', 'Whatever'))
    
    '''
    Create a new Device section and print the list of identifiers so as to see
    that the new identifier and position are included in identifiers
    '''
    a.make_section('Device', identifier='New Graphics Card')
    a.make_section('Screen', identifier='New Screeeeeeeeeen')
    print('\nIdentifiers after creating a new device section', a.identifiers)
    
    print('\nCreate Broken Screen section')
    pos = a.make_section('Screen', identifier='Broken Screen Section')
    print('\nAdding References')
    a.add_reference('Screen', 'Monitor', 'Broken Monitor Section', position=pos)
    a.add_reference('Screen', 'Device', 'Broken Device Section', position=pos)
    
    '''
    Try to fix section with broken references
    '''
    a.checkNFixSection('Screen', identifier='Broken Screen Section')
    '''
    Write the changes to the destination file
    '''
    a.writeFile(destination)

if __name__ == '__main__': main()
