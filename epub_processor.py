import os
from bs4 import BeautifulSoup
import re
import csv
import zipfile
from datetime import datetime
from epub_folder import classify_and_transfer_files

def get_all_epub_files(directory):
    """
    Find all *.epub from directory
    """
    epub_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.epub'):
                epub_files.append(os.path.join(root, file))
    return epub_files


def extract_ao3_epub_info(epub_path):
    """
    Extract AO3 standard info from epubs  
    """
    ao3_info = {
        'title': '',
        'author': '',
        'ao3_url': '',
        'rating': '',
        'warnings': '',
        'fandoms': '',
        'language': '',
        'published': '',
        'completed': '',
        'words': '',
        'chapters': '',
        'path': epub_path,
        'error': ''
    }

    try:
        with zipfile.ZipFile(epub_path, 'r') as zf:
            # 000.xhtml
            target_file = None
            for name in zf.namelist():
                if name.lower().endswith('.xhtml') and '000' in name:
                    target_file = name
                    break

            if not target_file:
                ao3_info['error'] = '000.xhtml not found'
                return ao3_info

            content = zf.read(target_file)
            soup = BeautifulSoup(content, 'lxml')

            # Title
            if soup.title and soup.title.string:
                title_text = soup.title.string.strip()
                m = re.match(r'(.+?) - (.+?) - (.+)', title_text)
                if m:
                    ao3_info['title'] = m.group(1).strip()
                    ao3_info['author'] = m.group(2).strip()
                    ao3_info['fandoms'] = m.group(3).strip()

            # work_url
            a_tag = soup.find('a', href=re.compile(r'archiveofourown\.org/works/'))
            if a_tag:
                ao3_info['ao3_url'] = a_tag['href']

            # tags
            dl = soup.find('dl', class_='tags')
            if dl:
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                for dt, dd in zip(dts, dds):
                    label = dt.text.strip().rstrip(':')
                    a_texts = [a.text.strip() for a in dd.find_all('a')]
                    value = ', '.join(a_texts) if a_texts else dd.get_text(strip=True)

                    if label == 'Rating':
                        ao3_info['rating'] = value
                    elif label == 'Archive Warning':
                        ao3_info['warnings'] = value
                    elif label == 'Language':
                        ao3_info['language'] = value
                    elif label == 'Stats':
                        stats_text = dd.get_text(separator=' ', strip=True)
                        published_match = re.search(r'Published:\s*(\d{4}-\d{2}-\d{2})', stats_text)
                        if published_match:
                            ao3_info['published'] = published_match.group(1)
                        completed_match = re.search(r'Completed:\s*(\d{4}-\d{2}-\d{2})', stats_text)
                        if completed_match:
                            ao3_info['completed'] = completed_match.group(1)
                        words_match = re.search(r'Words:\s*([\d,]+)', stats_text)
                        if words_match:
                            ao3_info['words'] = words_match.group(1)
                        chapters_match = re.search(r'Chapters:\s*([\d/]+)', stats_text)
                        if chapters_match:
                            ao3_info['chapters'] = chapters_match.group(1)

        return ao3_info

    except Exception as e:
        ao3_info['error'] = str(e)
        return ao3_info




def write_epub_metadata_to_csv(epub_paths, csv_path):
    """
    Make metadata csv  
    """
    fieldnames = [
        'path', 'title', 'author', 'ao3_url',
        'rating', 'warnings', 'fandoms', 'language',
        'published', 'completed', 'words', 'chapters', 'error'
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for epub_file in epub_paths:
            info = extract_ao3_epub_info(epub_file)
            row = {key: info.get(key, '') for key in fieldnames}
            writer.writerow(row)



def sanitize_filename(name,type=''):
    """
    Replace illegal filenames  
    """
    return re.sub(r'[\\/:*?"<>|]', type, name)

def rename_file(filepath, target_name):
    """
    Rename epubs  
    add _250101_1212 if duplicated  
    """
    try:
        directory = os.path.dirname(filepath)
        ext = os.path.splitext(filepath)[1]
        
        target_name_clean = sanitize_filename(target_name.strip())
        new_path = os.path.join(directory, target_name_clean + ext)

        # when new_path != original path, check if duplicate
        if new_path != filepath and os.path.exists(new_path):
            timestamp = datetime.now().strftime("_%y%m%d_%H%M%S")
            new_path = os.path.join(directory, target_name_clean + timestamp + ext)

        os.rename(filepath, new_path)
        # print(f"Rename succeeded: {filepath} -> {new_path}")
    
    except Exception as e:
        print(f"Failed rename {filepath}, Error: {e}")


def rename_from_csv(csv_path):
    """
    Rename *.epub from csv  
    """
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filepath = row.get('path')
                title = row.get('title')
                if filepath and title:
                    rename_file(filepath, title)
                else:
                    print(f"Invaild data: {row}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Rename
    directory = 'D:\\ao3file'
    csv_output_path = 'test.csv'
    epub_list = get_all_epub_files(directory)
    write_epub_metadata_to_csv(epub_list, csv_output_path)

    rename_from_csv("ao3_epub_metadata.csv")
    epub_list = get_all_epub_files(directory)
    write_epub_metadata_to_csv(epub_list, csv_output_path)

    classify_and_transfer_files(csv_path='ao3_epub_metadata.csv',classify_by="author",output_root=None,mode="move")

    # After sort
    directory_sorted = 'sorted_by_author'
    csv_output_path_sorted = 'ao3_sorted.csv'
    epub_list_sorted = get_all_epub_files(directory_sorted)
    write_epub_metadata_to_csv(epub_list_sorted, csv_output_path_sorted)
    rename_from_csv(csv_output_path_sorted)
    epub_list_sorted = get_all_epub_files(directory_sorted)
    write_epub_metadata_to_csv(epub_list_sorted, csv_output_path_sorted)

    print('end')