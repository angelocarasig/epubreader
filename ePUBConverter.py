from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re

'''
This Python file converts an epub into text. Requires path to epub.

Using main function 'convert(epub_path)':
'''

#TODO:
'''
- DONE! Image Support Per Chapter
- DONE! Purging Blank Chapters (Ones with just \n)
- Going to assume that the epubconverter strips each image into a seperate chapter. If not, i'm so fkd
'''

blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']

def image_support(path):
    '''
    Doesn't return anything.
    Collates all images inside the novel and places them in the novel's images folder.
    Numbered by when they appear in the novel (from 0)
    '''

    book = epub.read_epub(path)
    file_path = path[:path.rfind("\\") + 1]
    for index, image in enumerate(book.get_items_of_type(ebooklib.ITEM_IMAGE)):
        with open(f'{file_path}/images/image{index}.jpg','wb') as f:
            f.write(epub.EpubImage.get_content(image))

def chapters_list(epub_path) -> list: 
    '''
    Is used in loop with chapters_list to strip a chapter's contents to only text and image tags
    '''

    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chapter_contents(chap, file_path) -> list:
    '''
    Is used in loop with chapters_list to strip a chapter's contents to only text and image tags
    '''

    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    
    '''Writes to a file if the chapter contains an image'''
    #TODO: Deal with multiple images case
    images = soup.find_all('img')
    file_path = file_path[:file_path.rfind("\\") + 1]
    locations_file = f'{file_path}\\images\\locations.txt'

    if len(images) > 0:
        with open(locations_file,'a+') as f:
            f.write("1")
    else:
        with open(locations_file,'a+') as f:
            f.write("0")


    '''Cleaning up the mess'''
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def full_book(thtml, file_path) -> list:
    '''
    Generates a list with each index representing a section/chapter of the novel. 
    Note that images are considered as singular chapters
    '''

    output = []
    for html in thtml:
        text =  chapter_contents(html, file_path)
        output.append(text)
    return output

def convert(epub_path) -> list:
    '''
    Use this instead of the full_book function. 
    Does the same as full_book but also cleans extra whitespace and attaches the corresponding image tag to their respective locations.
    '''


    '''
    First purging locations if it exists for the book
    '''
    file_path = epub_path[:epub_path.rfind("\\") + 1]
    locations_file = f'{file_path}images\\locations.txt'
    with open(locations_file, "w") as f:
        f.write("")

    '''
    Generate first pass
    '''
    chapters = chapters_list(epub_path)
    final = full_book(chapters, epub_path)

    cleaned = []


    '''
    Check for whitespace only chapters before returning
    '''
    counter = 0
    for index, val in enumerate(final):
        print(index)
        with open(locations_file, "r") as f:
            curr = f.readline()
            print("INDEX: ", curr[index])
            if curr[index] == "1":
                final[index] += "\n"
                #<image src="{{ url_for('static', filename='BG.jpg')}}"/>
                cleaned.append("filename=\"{}images\image{}.jpg\"".format(file_path, counter))
                # cleaned.append(f"<img src=/>")
                counter += 1
        if final[index].isspace():
            print(final[index])
            print(f"Section {index} is a blank section. Removing...")
        elif final[index].strip() == "":
            print(final[index])
            print(f"Section {index} is a blank section. Removing...")
        else:
            #Converts multiple spaces into a single space due to previous methods stripping certain
            #parts of the section and leaving extra blank space
            cleaned.append(re.sub(' +', ' ', val))
            cleaned.append("\n=========\n") #TODO: Remove when chapters are properly seperated

    print("\n===Results===\n")
    print("File Path:", epub_path)
    print("Total Sections:", len(cleaned) // 2)
    print("=============")
    return cleaned

if __name__ == "__main__":
    pass