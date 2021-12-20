from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re
import urllib.request
import ePUBImageGenerator
blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']

def image_support(path):
    '''
    Doesn't return anything.
    Collates all images inside the novel and places them in the novel's images folder.
    Numbered by when they appear in the novel (from 0)
    '''
    ePUBImageGenerator.generate_images(path)

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
    For a section of the epub file, strip components to just text and image tags.\n
    string with byte-data --> string with text and image-tags\n
    Needs to be called in a for-loop for the chapters list
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

def _initialize_locations(epub_path) -> tuple:
    '''
    Initial processes:\n
    - Returns the locations file and file path as a tuple
    - Purges locations.txt if it exists for the book
    - 'file_path' variable directs to the epub file's directory --> where it's stored
    '''
    file_path = epub_path[:epub_path.rfind("\\") + 1]
    locations_file = f'{file_path}images\\locations.txt'
    with open(locations_file, "w") as f:
        f.write("")
    return locations_file, file_path

def _purge_whitespace(converted_epub_file, locations_file, file_path) -> list:
    '''
    PASS 1: Purge whitespace for each chapter in the book
    '''
    cleaned = []
    counter = 0
    for index, val in enumerate(converted_epub_file):
        print(index)
        with open(locations_file, "r") as f:
            curr = f.readline()
            print("INDEX: ", curr[index])
            if curr[index] == "1":
                converted_epub_file[index] += "\n"
                cleaned.append(" filename=\"{}images\image{}.jpg\"".format(file_path, counter))
                counter += 1
        if converted_epub_file[index].isspace():
            print(converted_epub_file[index])
            print(f"Section {index} is a blank section. Removing...")
        elif converted_epub_file[index].strip() == "":
            print(converted_epub_file[index])
            print(f"Section {index} is a blank section. Removing...")
        else:
            cleaned.append(re.sub(' +', ' ', val))

    return cleaned

def _check_external_imagelinks(first_pass_data, file_path):
    '''
    Searches for external image links within the epub file. If found, goes to site and downloads image.\n
    If links exist, it is *probably* an unofficial file.
    '''
    image_counter = 0
    for index, section in enumerate(first_pass_data):
        WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        links = re.findall(WEB_URL_REGEX, section)
        if len(links) > 0:
            for _ in range(len(links)):
                if links[0].find("jpg") >= 0 or links[0].find("png") >= 0:
                    print("Link: ", links[0])
                    section = section.replace(links[0], " filename=\"{}images\image{}.jpg\"\n".format(file_path, image_counter))
                    first_pass_data[index] = section
                    print("\nFound Link!!\n")
                    print("Link: \n", links[0])
                    print("Downloading...")
                    urllib.request.urlretrieve(links[0], f'{file_path}images\\image{image_counter}.jpg')
                image_counter += 1
                links.pop(0)
            print("\n\nSET FINISHED\n\n")
    return first_pass_data

def _rearrange_chapters(new, data, tag='filename='):
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
    return new

def convert_epub(epub_path) -> list:
    locations_file, file_directory = _initialize_locations(epub_path)
    #locations_file points to a locations.txt file 
    chapters = chapters_list(epub_path)
    final = full_book(chapters, epub_path)

    first_pass = _purge_whitespace(final, locations_file, file_directory)
    print("First pass: ", first_pass[0][:20])
    second_pass = _check_external_imagelinks(first_pass, file_directory)
    print("Second pass: ", second_pass[0][:20])

    third_pass = []

    cleaned_epub = _rearrange_chapters(new = third_pass, data = second_pass)
    return cleaned_epub

if __name__ == "__main__":
    pass