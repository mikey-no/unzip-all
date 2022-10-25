# Unzip all files

Unzip all zip files found based on input directory.

1) Searches through all subdirectories for zip files
2) For each zip file found creates a directory at that point in the hierarchy and a sub subdirectory with the name of 
the zip archive
3) Unzips the files in this sub subdirectory.
4) Repeats from 1 until there are no new zip files found

# For example:

### Input

```commandline
├───test-001
│   │   a file.txt
│   │
│   └───folder 1
│           b file.txt
│           folder 2.zip
```
Has ```folder 2.zip```

### Output 

```commandline
├───test-001                     
│   │   a file.txt               
│   │                            
│   └───folder 1
│       │   b file.txt
│       │   folder 2.zip
│       │
│       └───__unzip-all__
│           └───folder 2.zip
│               └───folder 2
│                   │   folder 3.zip
│                   │
│                   ├───folder 2a
│                   │   │   c file.txt
│                   │   │
│                   │   └───empty folder
│                   ├───folder 3
│       └───folder 2
│           ├───folder 2a
│           │   │   c file.txt
│           │   │
│           │   └───empty folder
│           └───folder 3
│                   d file.txt
│                   empty.txt
```
folder 2 was unzipped in
``` .\__unzip_all__\folder 2.zip\<unzipped here> ```
etc.

The programme run until there are no new zip files found to unzip.

Runs with python 3.10

The ```__unzip-all__``` folder name is set as a "constant" in the programme.

# To run
```commandline
cd unzip-all
python .\app\unzip-all.py --input-folder .\tests\test-files\test-001
```


# Test

Use the setup-test.bat file to re-set up the test files and folders.
The setup tests files folders only runs on Windows 10.
The re-run the programme as above.