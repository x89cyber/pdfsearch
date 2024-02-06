# pdfsearch
Search pdf files recursively for a specified search term starting at a specified search path.  If zip files are encountered in the search path that contain pdf files they will be extracted and searched.

### Requirements
#### Python
This script was developed with python3 and requires the ```tempfile``` and ```zipfile``` libraries.
#### Linux
This script uses ```pdftotext``` and ```grep``` to perform the search.

```
sudo apt-get update
sudo apt-get install poppler-utils
```

### Usage
```
python3 pdfsearch.py [starting directory] [search term]
```

### Output
If a match is found the path to the pdf file is output along with the line number and line text that contains the match.

### Cleanup
A temp directory is created under /tmp that is cleaned up before exiting.
