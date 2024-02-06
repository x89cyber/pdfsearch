#!/usr/bin/python3
import os
import sys
import subprocess
import tempfile
from zipfile import ZipFile

if (len(sys.argv) != 3):
    print(f"Usage: pdfsearch [starting dir] [search term]")
    exit(1)

starting_dir = sys.argv[1]
search_term = sys.argv[2]

def splash():
    ascii_art = '''

 ######################################################################
#             _  __                         _                          #
#            | |/ _|                       | |                         #
#   _ __   __| | |_ ___  ___  __ _ _ __ ___| |__                       #
#  | '_ \ / _` |  _/ __|/ _ \/ _` | '__/ __| '_ \                      #
#  | |_) | (_| | | \__ \  __/ (_| | | | (__| | | |                     #
#  | .__/ \__,_|_| |___/\___|\__,_|_|  \___|_| |_|                     #
#  | |                                                                 #
#  |_|                                                                 #
#                                                                      #
#  by x89cyber                                                         #  
#                                                                      #
#  ● Usage: pdfsearch.py [starting dir] [search term]                  #
#  ○ Uses pdftotext and grep to search pdf files for                   #
#    the specified search term                                         #
#  ○ Includes pdf's in zip archives                                    #
#                                                                      #
 ######################################################################
    '''
    print(ascii_art)
    print(f'[*] Searching {starting_dir} for "{search_term}"...')

def highlight(text, term, color):
    '''
    Highlight the term that appears in the text with the color specified: RED, ORANGE, LIME
    '''
    if (color == "RED"): 
        ht = text.replace(term, f'\033[1;31m{term}\033[0m')
    elif (color == "ORANGE"):
        ht = text.replace(term, f'\033[1m\033[38;5;208m{term}\033[0m')
    elif (color == "LIME"):
        ht = text.replace(term, f'\033[1;32m{term}\033[0m')
    else: return text
    return ht

def find_files(extension):
    '''
    Search for files ending in the specified extension.  ex. ".pdf"
    '''
    file_paths = []
    for root, dirs, files in os.walk(starting_dir):
        for file in files:
            if file.endswith(extension):
                file_paths.append(root + "/" + file)
    return file_paths

def search_pdf(pdf_file_path, temp_dir):
    '''
    Search pdf file for the search_term specified in the command line.  Uses pdftotext and grep.
    Outputs the file the term was found in and a snippet of the search result from grep.  Highlights the term.
    '''
    try:
        #use pdftotext to extract text from the PDF file and pipe it to grep for searching
        command = ["pdftotext", pdf_file_path, "-"]
        pdftotext_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        #use 'nl' to number lines and pipe the output to 'grep' for searching
        nl_command = ["nl", "-w1", "-s:"]  
        nl_process = subprocess.Popen(nl_command, stdin=pdftotext_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
       
        #use grep to search for preprocessed text
        grep_command = ["grep", search_term]
        grep_process = subprocess.Popen(grep_command, stdin=nl_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        pdftotext_process.stdout.close()  #close pdftotext stdout
        output, _ = grep_process.communicate() #perform the grep

        if output:
            pdf = pdf_file_path.replace(temp_dir, "") #remove the temp_dir from the file path if it is there (it is for extracted zip file)
            print(f"{highlight('[+]','[+]','ORANGE')} {pdf}:\n{highlight(output, search_term, 'RED')}", end="")  

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    splash()
    temp_dir = tempfile.mkdtemp() #create a temp directory for extracting zip files
    print(f'[*] Creating temp directory {temp_dir} for extracted zip files...')

    #find all zip files and pdf's in the starting directory 
    zips = find_files(".zip")
    pdfs = find_files(".pdf")
    
    #extract pdfs from zipfiles
    for z in zips:
        with ZipFile(z, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith(".pdf"):
                    zip_ref.extract(file_info, temp_dir + z)
                    pdfs.append(temp_dir + z + "/" + file_info.filename) #add to list of pdfs
    
    #search pdfs for the search term
    for p in pdfs:
        search_pdf(p, temp_dir)
    
    print(f'[*] Deleting temp directory {temp_dir} and all contents...')
    os.system('rm -fr temp_dir') #remove the temp directory
    print('[*] Your search is complete!')

if __name__ == "__main__":
    main()

