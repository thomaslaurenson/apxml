import os
import sys
import io
import apxml
import collections
import xml.dom.minidom

try:
    import Objects
except ImportError:
    print("Error: APXMLIntersection.py")
    print("       The Objects.py module is required to run this script")
    print("       You can download from: https://github.com/simsong/dfxml")
    print("       Now Exiting...")
    sys.exit(1)

################################################################################
# Intersection object
class Intersection(object):
    def __init__(self, profilesList):
        self.profileList = list()
        self.order = list()
        
        # DFXML and RegXML Objects to store FileObjects
        # and CellObjects found in the APXML documents
        self.dfxml_obj = Objects.DFXMLObject()
        self.regxml_obj = Objects.RegXMLObject()
        
        # Keep record of profile name for output
        self.out_fn = os.path.basename(profilesList[0])
        self.out_fn = os.path.splitext(self.out_fn)[0]

        # Parse each APXML file to a OrderedDict
        for i, profile in enumerate(profilesList):
            print("  > %s" % profile)
            apxml_obj = apxml.iterparse(profile)
            apxml.generate_stats(apxml_obj)
            # Split the file system path for the application profile
            name = profile.split('/')
            name = name[0]
            #name = name[len(name) - 1]
            #name = name.split("-")[0]
            apxml_obj.name = name
            self.profileList.append(apxml_obj)

    def sort_profiles(self, method):
        """ Sort profiles by selected method. """
        if method == None:
            pass
        elif method == "highest":
            self.profileList.sort(key=lambda x: x.stats.all, reverse=True)
        elif method == "lowest":
            self.profileList.sort(key=lambda x: x.stats.all, reverse=False)
        elif method == "stacked":
            self.profileList.sort(key=lambda x: x.stats.all, reverse=False)
            low = list(self.profileList)
            high = list(self.profileList)
            low.sort(key=lambda x: x.stats.all, reverse=False)
            high.sort(key=lambda x: x.stats.all, reverse=True)
            low = low[0:10]
            high = high[0:10]                       

            del self.profileList[:]
            for (h, l) in zip(high, low):
                self.profileList.append(h)
                self.profileList.append(l)
        
    def first_pass(self):
        """ Process the first profile """
        self.order.append(self.profileList[0])
        for obj in self.profileList[0]:
            if isinstance(obj, Objects.FileObject):
                obj.count = 1
                self.dfxml_obj.append(obj)
            if isinstance(obj, Objects.CellObject):
                obj.count = 1
                self.regxml_obj.append(obj)

    def next_pass(self, count):
        self.order.append(self.profileList[count])
        for obj in self.profileList[count]:
            match = False
            if isinstance(obj, Objects.FileObject):
                for fi in self.dfxml_obj:
                    if self.compare_files(fi, obj):
                        match = True
                        if fi.count is None:
                            obj.count = 1
                            self.dfxml_obj.append(obj)
                        else:
                            fi.count += 1
                if match == False:
                    obj.count = 1
                    self.dfxml_obj.append(obj)
            elif isinstance(obj, Objects.CellObject):
                for cell in self.regxml_obj:
                    if self.compare_cells(cell, obj):
                        match = True
                        if cell.count is None:
                            obj.count = 1
                            self.regxml_obj.append(obj)
                        else:
                            cell.count += 1
                if match == False:
                    obj.count = 1
                    self.regxml_obj.append(obj)


    def compare_files(self, fi1, fi2):
        """ Compare all metadata properties between two FileObjects (fi). """
        if fi1.filename.endswith(".lnk"):
            # Compare ShortCut (lnk) files
            # Do not compare SHA-1 hash value
            return (fi1.filename == fi2.filename and
                    fi1.meta_type == fi2.meta_type and
                    fi1.alloc_inode == fi2.alloc_inode and
                    fi1.alloc_name == fi2.alloc_name and
                    fi1.annos == fi2.annos and
                    fi1.app_state == fi2.app_state)
        
        elif fi1.filename.endswith(".pf"):
            # Normalize Prefetch file for comparison, e.g.,
            # Before: C:\Windows\Prefetch\TRUECRYPT.EXE-009A2E5A.pf
            # After:  C:\Windows\Prefetch\TRUECRYPT.EXE
            path1 = os.path.splitext(fi1.filename)[0]
            path1 = path1.split("-")[0]
            path2 = os.path.splitext(fi2.filename)[0]
            path2 = path2.split("-")[0]
            return (path1 == path2 and
                    fi1.meta_type == fi2.meta_type and
                    fi1.alloc_inode == fi2.alloc_inode and
                    fi1.alloc_name == fi2.alloc_name and
                    fi1.annos == fi2.annos and
                    fi1.app_state == fi2.app_state)
        
        # Default is to compare all object properties            
        return (fi1.filename == fi2.filename and
                fi1.meta_type == fi2.meta_type and
                fi1.sha1 == fi2.sha1 and
                fi1.alloc_inode == fi2.alloc_inode and
                fi1.alloc_name == fi2.alloc_name and
                fi1.annos == fi2.annos and
                fi1.app_state == fi2.app_state)

    def compare_cells(self, co1, co2):
        """ Compare all metadata properties between two CellObjects (co). """
        if "UserAssist" in co1.cellpath:
            return (co1.cellpath == co2.cellpath and
                co1.name_type == co2.name_type and
                co1.alloc == co2.alloc and
                co1.data_type == co2.data_type and
                co1.annos == co2.annos and
                co1.app_state == co2.app_state)
        return (co1.cellpath == co2.cellpath and
                co1.name_type == co2.name_type and
                co1.alloc == co2.alloc and
                co1.data_type == co2.data_type and
                co1.data == co2.data and
                co1.annos == co2.annos and
                co1.app_state == co2.app_state)

    def stats(self, count):
        fis = list(self.dfxml_obj)
        cos = list(self.regxml_obj)
        intersect_fis = [fi for fi in fis if fi.count == count + 1]
        intersect_cos = [co for co in cos if co.count == count + 1]

        cCOUNT = count + 1
        cALL = sum(1 for x in intersect_fis) + sum(1 for x in intersect_cos)
        cDIRS = len([fi for fi in intersect_fis if fi.meta_type == 2])
        cFILES = len([fi for fi in intersect_fis if fi.meta_type == 1])
        cKEYS = len([co for co in intersect_cos if co.name_type == "k"])
        cVALUES = len([co for co in intersect_cos if co.name_type == "v"])

        print("%s,%d,%d,%d,%s,%s \\\\ " % (self.order[count].name,
              cDIRS,
              cFILES,
              cKEYS,
              "{:,}".format(cVALUES),
              "{:,}".format(cALL)))

    def csv_output(self, count):
        # Create CSV for intersected entries
        count += 1
        files_csv = "n" + str(count) + "_FILES.csv"
        cells_csv = "n" + str(count) + "_CELLS.csv"
        # CSV for FILES
        with open(files_csv, 'w') as f:
            f.write("count,state,filename,delta,meta_type,alloc_name,alloc_inode,filesize,sha1\n")
            for fi in self.dfxml_obj:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (fi.count,
                                                          fi.app_state,
                                                          fi.filename,
                                                          "".join(fi.annos),
                                                          fi.meta_type,
                                                          fi.alloc_name,
                                                          fi.alloc_inode,
                                                          fi.filesize,
                                                          fi.sha1))
        # CSV for CELLS
        with open(cells_csv, 'w') as f:
            f.write("count,state,cellpath,delta,name_type,alloc,data_type,data\n")
            for co in self.regxml_obj:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (co.count,
                                                       co.app_state,
                                                       co.cellpath,
                                                       "".join(fi.annos),
                                                       co.name_type,
                                                       co.alloc,
                                                       co.data_type,
                                                       co.data))

    def apxml_output(self, count):
        # Reconstruct APXML document
        apxml_out = self.profileList[0]

        # Remove all files and cells from APXMLObject
        del apxml_out._files[:]
        del apxml_out._cells[:]

        # Append files and cells to new APXML
        for fi in self.dfxml_obj:
            if fi.count == count:
                apxml_out.append(fi)
        for cell in self.regxml_obj:
            if cell.count == count:
                apxml_out.append(cell)

        # Write a temp APXML document
        temp_fi = io.StringIO(apxml_out.to_apxml())
        # Format APXML using minidom
        xml_fi = xml.dom.minidom.parse(temp_fi)
        apxml_report = xml_fi.toprettyxml(indent="  ")
        # Set the file output name
        fn = self.out_fn + "-n" + str(count) + "-INTERSECTION.apxml"
        # Write out APXML document
        with open(fn, "w", encoding="utf-16-le") as f:
            #f.write("<?xml version='1.0' encoding='UTF-16' ?>")
            f.write(apxml_report)

################################################################################
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''APXMLIntersection.py''',
formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('profiles',
                        help = 'Application Profiles XML (APXML)',
                        nargs='+')
    parser.add_argument('mode',
                        help = 'How to store APXML order (none, lowest, highest, stacked)')                        
    args = parser.parse_args()

    obj = Intersection(args.profiles)

    # Sort profiles based on total number or digital artifacts
    # None = sorted based on argument position
    # lowest = sorted based on low > high
    # highest = sorted based on high > low
    obj.sort_profiles(args.mode)

    # Parse the first profile, and output
    obj.first_pass()
    print("profile_count,all,dirs,files,keys,values")
    obj.stats(0)
    obj.csv_output(0)

    # Parse each subsequent profile, and output
    count = 1
    profileCount = len(args.profiles)
    while count < profileCount:
        obj.next_pass(count)
        obj.stats(count)
        obj.csv_output(count)
        count += 1

    # Make an APXML document from final result
    obj.apxml_output(count)
