from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re
import urllib.request
import random

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

def new_sorter(new, data, tag='filename='):
    while len(data) > 0:
        curr = data[0]
        if curr.find(tag) < 0:
            print(f"IN SORTER: Didn't find anything for {curr[0:20]}")
            new.append(curr)
            data.pop(0)
        else:
            links = re.findall(tag, curr)
            if len(links) > 1: #If more than one link
                found = curr.find(tag)
                new.append(curr[:curr.find("\n", found)]) #Appends everything up to the thing
                data[0] = curr[curr.find("\n", found):] #Data is now 
            else:   #Only 1 link
                print(curr)
                new.append(curr)
                data.pop(0)

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
    PASS 1: Check for whitespace only chapters before returning
    '''
    counter = 0
    for index, val in enumerate(final):
        print(index)
        with open(locations_file, "r") as f:
            curr = f.readline()
            print("INDEX: ", curr[index])
            if curr[index] == "1":
                final[index] += "\n"
                cleaned.append(" filename=\"{}images\image{}.jpg\"".format(file_path, counter))
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
            # cleaned.append("\n=========\n") #TODO: Remove when chapters are properly seperated

    '''
    PASS 2: Check for jpg/png hyperlinks
    '''
    image_counter = 0
    for index, section in enumerate(cleaned):
        WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        links = re.findall(WEB_URL_REGEX, section)
        if len(links) > 0:
            for _ in range(len(links)):
                if links[0].find("jpg") >= 0 or links[0].find("png") >= 0:
                    print("Link: ", links[0])
                    section = section.replace(links[0], " filename=\"{}images\image{}.jpg\"\n".format(file_path, image_counter))
                    cleaned[index] = section
                    urllib.request.urlretrieve(links[0], f'{file_path}images\\image{image_counter}.jpg')
                image_counter += 1
                links.pop(0)
            print("\n\nSET FINISHED\n\n")
    
    print("CLEANED LENGTH: ", len(cleaned))

    pass2_temp = []
    new_sorter(new=pass2_temp, data=cleaned, tag="filename=")



    '''
    Chapter seperation viewer. Comment out when chapters are fully processed into proper sections.
    '''
    pass3_temp = []
    for i in pass2_temp:
        pass3_temp.append(i)
        pass3_temp.append("=" * 15)

    return pass3_temp

if __name__ == "__main__":
    import os
    #TODO: FIX IMAGES THAT ARE LINKED VIA WEBPAGE
    # Do a 2nd pass that searches for images that are tagged jpg/png etc.
    # Replace with a incrementing filename=... 
    # Split above text to its own list element
    # 
    
    # book = epub.read_epub("book.epub")
    # for item in book.get_items():
    #     if item.get_type() == ebooklib.ITEM_DOCUMENT:
    #         print(item.get_content())