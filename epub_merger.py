import os
import uuid
from ebooklib import epub, ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, ITEM_FONT
from bs4 import BeautifulSoup

def find_epubs_in_dir(dir_path):
    epub_list = [
        os.path.abspath(os.path.join(dir_path, f))
        for f in os.listdir(dir_path)
        if f.endswith('.epub') and os.path.isfile(os.path.join(dir_path, f))
    ]
    return epub_list

def get_title(book):
    title = book.get_metadata('DC', 'title')
    return title[0][0] if title else 'Untitled'


def get_preface_and_chapters(book):
    items = list(book.get_items_of_type(ITEM_DOCUMENT))
    if not items:
        return None, []

    # split_xxx.xhtml
    xhtml_items = sorted(
        [item for item in items if item.file_name.endswith(".xhtml") and "split_" in item.file_name],
        key=lambda x: x.file_name
    )

    if len(xhtml_items) < 3:
        return None, []

    preface = xhtml_items[0]  # split_000
    chapter_items = xhtml_items[2:-1] if len(xhtml_items) > 4 else []  # [2:-1] delete afterwords

    chapters = []
    for i, item in enumerate(chapter_items, start=1):
        soup = BeautifulSoup(item.get_content(), 'lxml')
        h2 = soup.find('h2', class_='heading')
        title = h2.get_text().strip() if h2 else f"Chapter {i}"
        chapters.append((title, item))

    return preface, chapters


def merge_original(epub_paths, output_path, merged_title):
    """
    Default merge EPUB files  
    Do not change any styles of EPUBs  
    """
    merged_book = epub.EpubBook()
    merged_book.set_identifier(str(uuid.uuid4()))
    merged_book.set_title(merged_title)
    merged_book.set_language('zh')

    merged_book.add_item(epub.EpubNav())
    merged_book.add_item(epub.EpubNcx())

    spine = ['nav']
    toc = []

    for index, epub_file in enumerate(epub_paths):
        book = epub.read_epub(epub_file)
        title = get_title(book)
        prefix = f"book{index}_"

        preface, chapters = get_preface_and_chapters(book)

        if not preface:
            print(f"{epub_file} has no valid chapter")
            continue

        section_items = []

        for item in book.items:
            if item.get_type() == ITEM_DOCUMENT and item.file_name.endswith(".xhtml"):
                # skip afterword in [-1]
                if "split" in item.file_name and any(item.file_name.endswith(f"split_{i:03}.xhtml") for i in range(100, 999)):
                    continue

                item.id = prefix + item.id
                item.file_name = prefix + item.file_name
                merged_book.add_item(item)
                section_items.append(item)
            elif item.get_type() == ITEM_IMAGE or item.get_type() == ITEM_STYLE:
                item.id = prefix + item.id
                item.file_name = prefix + item.file_name
                merged_book.add_item(item)

        preface_file = preface.file_name if preface else section_items[0].file_name

        # TOC nav
        if chapters:
            subitems = []
            for ch_title, ch_item in chapters:
                subitems.append(epub.Link(ch_item.file_name, ch_title, ch_item.id))
            toc.append((epub.Link(preface_file, title, prefix + "toc"), subitems))
        else:
            toc.append(epub.Link(preface_file, title, prefix + "toc"))

        spine.extend(section_items)

    merged_book.spine = spine
    merged_book.toc = toc
    epub.write_epub(output_path, merged_book)
    print(f"✅ Merge completed: {output_path}")

def read_file_paths(txt_path):
    file_paths = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            path = line.strip()
            if path:
                file_paths.append(path)
    return file_paths    

if __name__ == "__main__":
    epub_list = read_file_paths(txt_path='')
    dir = r'input your dir here'
    epub_list = find_epubs_in_dir(dir)
    print(epub_list)        

    merge_original(epub_list, "output_original.epub", "AO3 collection Original")
