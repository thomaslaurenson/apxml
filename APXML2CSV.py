import os

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
    
################################################################################    
def make_csv_files(files):
    # Create CSV for file system entries
    files_csv = "files.csv"
    
    with open(files_csv, 'w') as f:
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("app_name",
                                                           "app_state",
                                                           "annos",
                                                           "filename",
                                                           "filename_norm",
                                                           "basename",
                                                           "basename_norm",
                                                           "filesize",
                                                           "meta_type",
                                                           "alloc_name",
                                                           "alloc_inode",
                                                           "sha1"))
        for fi in files:
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (fi.app_name,
                                                               fi.app_state,
                                                               fi.annos,
                                                               fi.filename,
                                                               fi.filename_norm,
                                                               fi.basename,
                                                               fi.basename_norm,
                                                               fi.filesize,
                                                               fi.meta_type,
                                                               fi.alloc_name,
                                                               fi.alloc_inode,
                                                               fi.sha1))
                                                               
def make_csv_cells(cells):
    # Create CSV for Registry entries
    cells_csv = "cells.csv"
    
    with open(cells_csv, 'w') as f:
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("app_name",
                                                        "app_state",
                                                        "annos",
                                                        "cellpath",
                                                        "cellpath_norm",
                                                        "basename",
                                                        "basename_norm",
                                                        "alloc",
                                                        "data_type",
                                                        "data",
                                                        "data_raw"))
        for co in cells:
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (co.app_name,
                                                            co.app_state,
                                                            co.annos,
                                                            co.cellpath,
                                                            co.cellpath_norm,
                                                            co.basename,
                                                            co.basename_norm,
                                                            co.alloc,
                                                            co.data_type,
                                                            co.data,
                                                            co.data_raw))     

    
################################################################################
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''APXML2CSV.py''',
formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('profile',
                        help = 'Application Profile XML (APXML)')                       
    args = parser.parse_args()

    files = list()
    cells = list()

    apxml_obj = apxml.iterparse(args.profile)

    for obj in apxml_obj:
        if isinstance(obj, Objects.FileObject):
            files.append(obj)
        if isinstance(obj, Objects.CellObject):
            cells.append(obj)
            
    make_csv_files(files)
    make_csv_cells(cells)
