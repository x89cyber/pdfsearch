# pdfsearch
Search pdf files and pdf files in zip archives

### Requirements
#### Python
This script was developed with python3 and requires the tempfile and zipfile libraries
#### Linux
This script uses pdftotext and grep to perform the searching at the OS level

### Usage
python3 pdfsearch.py [starting directory] [search term]

### Cleanup
A temp directory is created under /tmp the is cleaned up before exiting
