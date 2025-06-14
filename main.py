from epub_folder import *
from epub_processor import *
from epub_merger import *

def main():
    print("Please choose function")
    print("1. Generate a csv file with all epub information")
    print("2. Rename all epub formattedly, NEED RUN 1 to generate a csv first!!!Will update the csv file after rename")
    print("3. Sort and move or copy all epub by author or language, need a formatted csv file from 1 or 2")
    print("4. Generate a merged epub from multiple ao3 epubs")
    choice = input("Please input func choice(1/2/3/4)").strip()

    if choice == '1':
        print('Input param:\ndirectory = The directory for unsorted ao3 epubs, e.g:D://ao3file\ncsv_output_path = Output csv file name and path, e.g = ao3_epub_metadata.csv')
        directory = input("The directory for unsorted ao3 epubs: \n").strip()
        csv_output_path = input("Output csv file name and path: \n").strip()
        # csv_output_path = 'ao3_epub_metadata.csv'
        epub_list = get_all_epub_files(directory)
        print(f"Found {len(epub_list)} epub files in {directory}")
        write_epub_metadata_to_csv(epub_list, csv_output_path)
        print(f'Saved info of all epub in {directory} to {csv_output_path}\n')

    elif choice == '2':
        print('NEED RUN 1 to generate a csv first!!!\nWill update the csv file after rename')
        print('Input param:\ndirectory = The directory for unsorted ao3 epubs, e.g:D://ao3files\ncsv_output_path = Output csv file name and path, e.g = ao3_epub_metadata.csv')
        directory = input("The directory for unsorted ao3 epubs: \n").strip()        
        csv_output_path = input("Input generated csv file from func 1: \n").strip()

        rename_from_csv(csv_output_path)
        epub_list = get_all_epub_files(directory)
        write_epub_metadata_to_csv(epub_list, csv_output_path)

        print(f'Finished rename, updated csv{csv_output_path} and all epubs in {directory}')

    elif choice == '3':
        print('NEED RUN 1 or 2 to generate a csv first!!!\nWill update the csv file after rename')  
        print("Param example:\ncsv_path = ao3_epub_metadata.csv\nmode = copy\nclassify_by = author\noutput_root=D://dir")
        csv_path = input("Output csv file name and path: \n").strip()
        mode = input("Input move or copy: \n").strip()
        classify_by = input("Input classify file method, e.g: author, language: \n").strip()
        output_root = input("Input output directory: \n").strip()

        classify_and_transfer_files(csv_path,classify_by,output_root,mode)   

        directory_sorted = output_root

        csv_output_path_sorted = 'ao3_sorted.csv'
        epub_list_sorted = get_all_epub_files(directory_sorted)
        write_epub_metadata_to_csv(epub_list_sorted, csv_output_path_sorted)
        rename_from_csv(csv_output_path_sorted)
        epub_list_sorted = get_all_epub_files(directory_sorted)
        write_epub_metadata_to_csv(epub_list_sorted, csv_output_path_sorted)
        print(f'Finished sorting, new csv = ao3_sorted.csv, and sorted files in {directory_sorted}')
    elif choice == '4':
        print("Param example:\ntxt_path = D//:1.txt\noutput_path = D://dir//merged_epub.epub\nmerged_title=Ao3 merged file")
        txt_path = input("Input a txt path with all the ao3 files with ORDER that you want to merge into 1 file: \n").strip()
        output_path = input("Input merged file path: \n").strip()
        merged_title = input("Input merged epub file title: \n").strip()

        epub_list = read_file_paths(txt_path)    
        merge_original(epub_list, output_path, merged_title)
        print(f'Finished merge, file in {output_path}')
    else:
        print("Invalid input choice")

if __name__ == '__main__':
    main()