# AO3 EPUB TOOLS 
  
This toolset helps process and organize .epub files downloaded from Archive of Our Own (AO3). It includes functions to extract metadata, rename files, sort files by author or language, and merge multiple EPUBs into a single collection.

## Features  
1. **Extract Metadata to CSV**  

Parse a folder of AO3 .epub files and generate a .csv file containing metadata (e.g., title, author, tags, summary, etc.).  

2. **Rename EPUB Files (based on metadata)**  

Automatically rename all .epub files using standardized formats, updating the CSV after renaming.

3. **Sort and Copy/Move EPUBs**  

Organize .epub files into subfolders (by author or language), optionally copying or moving them. Also updates metadata and file names.

4. **Merge Multiple EPUBs into One**  

Merge several AO3 .epub files into a single EPUB file (e.g., a collection or themed bundle), preserving chapter order.

## How to Use
Run with .bat (Recommended)
You can launch the tool by running the provided run.bat file, which calls main() in main.py.

Interactive Options
When running, you'll see:
```
Please choose function
1. Generate a csv file with all epub information
2. Rename all epub formattedly
3. Sort and move or copy all epub by author or language
4. Generate a merged epub from multiple ao3 epubs
```
## Function Usage
1. **Extract EPUB Info to CSV**

Input:
  directory = Folder with AO3 .epub files (e.g. D://ao3files)  
  csv_output_path = Output .csv file path (e.g. ao3_epub_metadata.csv)  

2. **Rename EPUB Files**  

Requires CSV file from step 1.  
Will rename files using title/author, and update the CSV accordingly.  

3. **Sort and Move/Copy EPUBs**  

Requires CSV file from step 1 or 2.
Input:
  csv_path = Metadata .csv file  
  mode = 'copy' or 'move'  
  classify_by = 'author' or 'language'  
  output_root = Destination folder (e.g. D://sorted_epubs)  

4. **Merge EPUBs**  

Input:  
  txt_path = .txt file listing EPUB file paths (one per line, in desired merge order)  
  output_path = Output merged EPUB file path  
  merged_title = Title of merged EPUB file  

## Generate AZW3  
Please install `calibre`  
And write your calibre install path into `convert_to_azw3.bat`  
```
set CONVERTER="C:\Program Files\Calibre2\ebook-convert.exe"
```  
Put epub files that you want to convert in the directory `convert`  
Then run `convert_to_azw3.bat`  
## ⚠️ Notes
Only works with .epub files from AO3.  
Calibre or other .epub readers can help preview results.
Ensure encoding is UTF-8 when using external text files.

## 📌 License
This project is for personal, educational, or archiving use only. Respect AO3’s Terms of Service and do not use this to redistribute works without permission.