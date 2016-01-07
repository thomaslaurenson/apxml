# apxml

APXML is a forensic data abstraction deisgned to store digital artifacts (directories, data files, Registry keys and Registry values) associated with application software. A Python API (apxml.py) is provided to automate processing of the contents of APXML documents. This repository also contains a varity of sample programs to automate processing of APXML documents.

## Applicatoin Profile XML (APXML)

Application Profile XML (APXML) is a hybrid forensic data abstraction based on Digital Forensic XML (DFXML) and Registry XML (RegXML). The overall structure of an APXML document displayed in the following code snippet:

```
<apxml>
  <metadata/>
  <creator/>
   <!-- DFXML FileObjects -->
   <!-- RegXML CellObjects -->
   <rusage/>
</apxml>
```

Basically, APXML stored file system entries as DFXML FileObjects and Windows Registry entries as RegXML CellObjects.

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
