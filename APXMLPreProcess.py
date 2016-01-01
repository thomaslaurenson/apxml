#!/usr/bin/env python3

"""
Author:  Thomas Laurenson
Email:   thomas@thomaslaurenson.com
Website: thomaslaurenson.com
Date:    2015/12/31

Description:
The APXMLPreProcess.py Python module takes an APXML document as input
and pre-processes the document for processing against a target data
set.

Copyright (c) 2015, Thomas Laurenson

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

>>> CHANGELOG:
    0.1.0       Base functionality ()

"""

import os
import io
import collections
import xml.dom.minidom

try:
    import dfxml
except ImportError:
    print("Error: apxml.py")
    print("       The dfxml.py module is required to run this script")
    print("       You can download from: https://github.com/simsong/dfxml")
    print("       Now Exiting...")
    sys.exit(1)

try:
    import Objects
except ImportError:
    print("Error: apxml.py")
    print("       The Objects.py module is required to run this script")
    print("       You can download from: https://github.com/thomaslaurenson/apxml")
    print("       Now Exiting...")
    sys.exit(1)

try:
    import apxml
except ImportError:
    print("Error: apxml.py")
    print("       The apxml.py module is required to run this script")
    print("       You can download from: https://github.com/thomaslaurenson/apxml")
    print("       Now Exiting...")
    sys.exit(1)

try:
    import FilePathNormalizer
except ImportError:
    print('Error: APXMLFinalise.py')
    print('       The FilePathNormalizer.py module is required.')
    print('       You can download from: https://github.com/thomaslaurenson/Vestigium')
    print('       Now Exiting...') 
    sys.exit(1)

try:
    import CellPathNormalizer
except ImportError:
    print('Error: APXMLFinalise.py')
    print('       The CellPathNormalizer.py module is required.')
    print('       You can download from: https://github.com/thomaslaurenson/Vestigium')
    print('       Now Exiting...') 
    sys.exit(1)
    
# Initialize the file path normalizer object
file_path_normalizer = FilePathNormalizer.FilePathNormalizer()

# Initialize the cell path normalizer object
cell_path_normalizer = CellPathNormalizer.CellPathNormalizer()

# Create DFMXL and RegXML Objects to store information
dfxml = Objects.DFXMLObject()
regxml = Objects.RegXMLObject() 

def normalise_all(apxml_obj):
    for obj in apxml_obj:
        if isinstance(obj, Objects.FileObject):
            # Add basename to FileObject
            basename = obj.filename.split("\\")
            obj.basename = basename[len(basename) - 1]
            
            # Normalize the file path and append to FileObject
            obj.filename_norm = file_path_normalizer.normalize(obj.filename) 
            
            # Use filename_norm to extract basename_norm
            basename_norm = obj.filename_norm.split("/")
            obj.basename_norm = basename_norm[len(basename_norm) - 1]

            # LiveDiff stores SHA-1 hashes in uppercase, convert to lower
            if obj.sha1 is not None:
                obj.sha1 = obj.sha1.lower()
            obj.app_name = apxml_obj.metadata.app_name     
            
            # Add a orphan_name to only unallocated files
            if not obj.is_allocated() and obj.meta_type == 1:
                split = obj.filename.split("\\")
                obj.orphan_name = "$OrphanFiles/" + split[len(split) - 1]            
            
            # All done, append to DFXMLObject
            dfxml.append(obj)
                        
        elif isinstance(obj, Objects.CellObject):           
            # Normalize the cell path
            obj.cellpath_norm = cell_path_normalizer.normalize_profile_co(obj.cellpath)
            rootkey = obj.cellpath_norm.split("\\")[0]
            obj.cellpath_norm = cell_path_normalizer.normalize_target_co(obj.cellpath_norm, rootkey)
                    
            # Normalize the basename
            obj.basename_norm = None
            if obj.basename and obj.basename.startswith("C:"):
                normbasename = file_path_normalizer.normalize(obj.basename)
                normbasename = normbasename.replace('/', '\\')
                obj.basename_norm = normbasename
                obj.cellpath_norm = obj.cellpath_norm.replace(obj.basename, obj.basename_norm)               
            regxml.append(obj)
                
def apxml_output(apxml_obj, fn):
    # Reconstruct APXML document
    apxml_out = apxml_obj

    # Set the output filename based on profile
    fn = os.path.basename(fn)
    fn = os.path.splitext(fn)[0]
    
    # Remove all files and cells from APXMLObject
    del apxml_out._files[:]
    del apxml_out._cells[:]

    # Append files and cells to new APXML
    for fi in dfxml:
        apxml_out.append(fi)
    for cell in regxml:
        apxml_out.append(cell)

    # Write a temp APXML document
    temp_fi = io.StringIO(apxml_out.to_apxml())
    # Format APXML using minidom
    xml_fi = xml.dom.minidom.parse(temp_fi)
    apxml_report = xml_fi.toprettyxml(indent="  ")
    # Set the file output name
    out_fi = fn + "-NORM.apxml"
    
    # Write out APXML document
    with open(out_fi, "w", encoding="utf-16-le") as f:
        #f.write("<?xml version='1.0' encoding='UTF-16' ?>")
        f.write(apxml_report)        
        
            
            
################################################################################
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''APXMLPreProcess.py''',
formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('profile',
                        help = 'Application Profile XML (APXML)')              
    args = parser.parse_args()

    apxml_obj = apxml.iterparse(args.profile)
    apxml.generate_stats(apxml_obj)

    normalise_all(apxml_obj) 
    apxml_output(apxml_obj, args.profile) 
