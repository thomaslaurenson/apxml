#!/usr/bin/env python3

"""
Author:  Thomas Laurenson
Email:   thomas@thomaslaurenson.com
Website: thomaslaurenson.com
Date:    2016/02/22

Description:
The APXMLPrintStats.py Python module print statistics for an APXML document.

Copyright (c) 2016, Thomas Laurenson

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
import apxml
import Objects

try:
    import dfxml
except ImportError:
    print("Error: APXMLPrintStats.py")
    print("       The dfxml.py module is required to run this script")
    print("       You can download from: https://github.com/simsong/dfxml")
    print("       Now Exiting...")
    sys.exit(1)

try:
    import Objects
except ImportError:
    print("Error: APXMLPrintStats.py")
    print("       The Objects.py module is required to run this script")
    print("       You can download from: https://github.com/thomaslaurenson/apxml")
    print("       Now Exiting...")
    sys.exit(1)

try:
    import apxml
except ImportError:
    print("Error: APXMLPrintStats.py")
    print("       The apxml.py module is required to run this script")
    print("       You can download from: https://github.com/thomaslaurenson/apxml")
    print("       Now Exiting...")
    sys.exit(1)

###############################################################################
SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KB', 'MB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size to human-readable form.

    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000

    Returns: string

    '''
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')

################################################################################
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''APXMLPrintStats.py.''',
formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('profile',
                        help = 'profile')
                    
    args = parser.parse_args()
    
    fi = args.profile
    
    apxml_obj = apxml.iterparse(fi)
    apxml.generate_stats(apxml_obj)
    
    if apxml_obj.rusage.end_date is not None:
        processing_time = apxml_obj.rusage.end_date - apxml_obj.creator.execution_environment.start_date
        time = int(processing_time.total_seconds())    
    
    filesize = os.stat(fi)
    ap_filesize = approximate_size(filesize.st_size)
    
    name = os.path.basename(fi)
    
    print("%s & %s & %s & %s & %s & %s & %s & %s \\\\ " % (name,
                         "{:,}".format(apxml_obj.stats.dirs),
                         "{:,}".format(apxml_obj.stats.files),
                         "{:,}".format(apxml_obj.stats.keys),
                         "{:,}".format(apxml_obj.stats.values),
                         "{:,}".format(apxml_obj.stats.all),
                         time,
                         ap_filesize))               
