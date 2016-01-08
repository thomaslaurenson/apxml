# apxml

APXML is a forensic data abstraction deisgned to store digital artifacts (directories, data files, Registry keys and Registry values) associated with application software. A Python API (apxml.py) is provided to automate processing of the contents of APXML documents. This repository also contains a varity of sample programs to automate processing of APXML documents.

## Application Profile XML (APXML)

Application Profile XML (APXML) is a hybrid data abstraction based on Digital Forensic XML (DFXML) and Registry XML (RegXML) forensic data abstractions. The overall structure of an APXML document displayed in the following code snippet:

```
<apxml>
  <metadata/>
  <creator/>
   <!-- DFXML FileObjects -->
   <!-- RegXML CellObjects -->
   <rusage/>
</apxml>
```

Basically, APXML stores file system entries as DFXML FileObjects and Windows Registry entries as RegXML CellObjects. Additional metadata, creator and rusage XML elements store application profile information.

Example of a populated FileObject:

```
  <fileobject delta:new_file="1">
    <filename>C:\Program Files\TrueCrypt\TrueCrypt Setup.exe</filename>
    <filename_norm>%PROGRAMFILES%/TrueCrypt/TrueCrypt Setup.exe</filename_norm>
    <basename>TrueCrypt Setup.exe</basename>
    <basename_norm>TrueCrypt Setup.exe</basename_norm>
    <filesize>3466248</filesize>
    <alloc_inode>1</alloc_inode>
    <alloc_name>1</alloc_name>
    <meta_type>1</meta_type>
    <hashdigest type="sha1">7689d038c76bd1df695d295c026961e50e4a62ea</hashdigest>
    <app_name>TrueCrypt</app_name>
    <app_state>install</app_state>
  </fileobject>
```

Example of a populated CellObject:

```
  <cellobject delta:new_cell="1">
    <cellpath>HKLM\SOFTWARE\Classes\.tc\(Default)</cellpath>
    <cellpath_norm>SOFTWARE\Classes\.tc\(Default)</cellpath_norm>
    <basename>(Default)</basename>
    <name_type>v</name_type>
    <alloc>1</alloc>
    <data_type>REG_SZ</data_type>
    <data>TrueCryptVolume</data>
    <data_raw>54 00 72 00 75 00 65 00 43 00 72 00 79 00 70 00 74 00 56 00 6F 00 6C 00 75 00 6D 00 65 00 00 00</data_raw>
    <app_name>TrueCrypt</app_name>
    <app_state>install</app_state>
  </cellobject>
```

## Generating APXML Documents

LiveDiff is a portable Windows differencing tool to perform system-level reverse engineering. It was designed specifically to perform differential forensic analysis of application software, a type of system-level reverse engineering. The output of execution of LiveDiff is an APXML document populated with digital artifacts (directories, data files, Windows Registry keys and values) that are associated with an application.

## Reading APXML Documents
The apxml.py module has the functionality to parse and APXML document and generate a variety of Python objects that represent the contents of the document. An APXML document can be processed using the following Python code:

```
# Import apxml module
import apxml
# Read the APXML document using iterparse
apxml_obj = apxml.iterparse("TrueCrypt.apxml")
```

The following Python code can read an APXML document and print the full path and SHA-1 hash value of each data file in an APXML document.

```
# Import apxml module
import apxml

# Read the APXML document using iterparse
apxml_obj = apxml.iterparse("TrueCrypt.apxml")

# Loop through each object and print file name and SHA-1 hash value
for fi in apxml_obj:
    if isinstance(fi, Objects.FileObject) and fi.meta_type == 1:
        print(fi.filename, fi.sha1)
```
