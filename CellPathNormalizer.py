# !/usr/bin/python

"""
Author:  Thomas Laurenson
Email:   thomas@thomaslaurenson.com
Website: thomaslaurenson.com
Date:    2015/12/28

Description:
CellPathNormalizer.py is a Vestigium module to normalize the full path
of a Windows Registry artifact.

Copyright (c) 2015, Thomas Laurenson

###############################################################################
This file is part of Vestigium.

Vestigium is free software: you can redistribute it and/or modify
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
"""

__version__ = "1.0.0"

import codecs

try:
    import FilePathNormalizer
except ImportError:
    print('Error: CellPathNormalizer.py')
    print('       The FilePathNormalizer.py module is required.')
    print('       You can download from: https://github.com/thomaslaurenson/Vestigium')
    print('       Now Exiting...')
    sys.exit(1)

################################################################################
class CellPathNormalizer():
    def __init__(self):
        """ Initialise CellPathNormalizer object. """
        self.file_path_normalizer = FilePathNormalizer.FilePathNormalizer()
        self.active_rootkey = None

    def normalize_profile_co(self, cellpath):
        """ Normalize the cellpath of the Profile CellObject (PCO). """
        normpath = cellpath
        # Remove Registry hive naming convention
        if normpath.startswith("HKLM\\"):
            normpath = normpath[5:]
        if normpath.startswith("HKU\\"):
            normpath = normpath[4:]
            normpath = normpath.split("\\")
            del normpath[0]
            normpath = "\\".join(normpath)
            normpath = "NTUSER.DAT\\" + normpath
        return normpath

    def normalize_rootkey(self, cellpath, rootkey):
        """
        Normalize the cellpath rootkey of the Target CellObject (TCO), e.g.,
        Before: CMI-CreateHive{F10156BE-0E87-4EFB-969E-5DA29D131144}\ControlSet001\
        After:  SYSTEM\ControlSet001\
        """
        # Normalise hive rootkey, or return if None
        if cellpath:
            normpath = cellpath.split("\\")
            normpath[0] = rootkey
            normpath = "\\".join(normpath)
            return normpath
        else:
            return cellpath

    def normalize_cellpath(self, cellpath, rootkey):
        """ Normalize the cellpath of the Target CellObject (TCO). """
        
        # Split a cellpath on backslashes, or return if None
        if cellpath:
            normpath = cellpath.split("\\")
        else:
            return cellpath

        # System hive normalisation
        if rootkey == "system":
            control_names = ["controlset001",
                             "controlset002",
                             "controlset003",
                             "currentcontrolset",
                             "clone"]
            # If path has "control set" name, normalise target path
            # See: http://support.microsoft.com/kb/100010
            #for name in control_names:
            if len(normpath) >= 2:
                if normpath[1] in control_names:
                    normpath[1] = "%controlset%"

        # Join the split normalised path and return
        normpath = "\\".join(normpath)
        return normpath

    def normalize_basename(self, basename):
        """ If the basename is a path, normalize using the normalize function
            from the FilePathNormalizer module. """
       
        basename_norm = None
        
        # Decrypt a UserAssist entry ('P:' equates to 'C:' using rot13) 
        if basename.startswith("P:"):
            basename_norm = codecs.decode(obj.basename, "rot_13")
   
        # Strip UserAssist prefix in older windows versions
        elif basename.startswith("HRZR_EHACNGU"):
            basename_norm = basename[12:]
        
        else:
            basename_norm = basename
    
        # If basename_norm starts with C:
        if basename_norm.startswith("C:"):
            basename_norm = basename_norm[3:]
        
        # Replace backslash with forward slash
        basename_norm = basename_norm.replace('\\', '/')
        
        # Now normlaise using file path normaliser modules
        basename_norm = self.file_path_normalizer.normalize(basename_norm)

        return basename_norm
