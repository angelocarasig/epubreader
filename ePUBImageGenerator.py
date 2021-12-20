import ebooklib
from ebooklib import epub
import re

def generate_images(book_location):
    '''Requires path to epub file as a parameter.'''
    book = epub.read_epub(book_location)

    data = _store_imagetitles_in_list(book)

    _sort_nicely(data)

    image_directory = book_location[:book_location.rfind("\\") + 1]

    for index, image_name in enumerate(data):
        for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if image_name == image.get_name():
                # print(f"Image{index}: {image.get_name()}")
                with open(f'{image_directory}/images/image{index}.jpg','wb') as f:
                        f.write(epub.EpubImage.get_content(image))

def _tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
    
def _alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ _tryint(c) for c in re.split('([0-9]+)', s) ]

def _sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=_alphanum_key)

def _store_imagetitles_in_list(book):
    data = []
    for file_type in book.get_items():
        if type(file_type) == epub.EpubImage:
            for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                if file_type == image:
                    data.append(image.get_name())
    return data