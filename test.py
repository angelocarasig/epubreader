# import re

# string = "hey http://www.google.com.jpg xd www.youtube.com asdasdas  https://confusedtls.files.wordpress.com/2020/07/ln_2nd_vol_01-03.jpg?w=1618 "

# WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
# re.findall(WEB_URL_REGEX, string)
import enum
import re

import ebooklib


# for index, val in enumerate(data):
#     found = val.find(a)
#     print("Found: ", found)
#     if found >= 0:
#         while found >= 0:
#             print(f"Adding:\n===\n {val[found:]} \n===\n to new...")
#             print("\n========\n")
            
#             new.append(val[found:])
#             print(f"Replacing val with  {val[:found]}...")
            
#             val = val[:found]
#             found = val.find(a)
            
#             print("Newly added: ", new)
        
# print(len(new))

a = "filename="

# data = [
#     "filename=\"static\\uploads\\Classroom of the Elite 2nd Year - Volume 1\\images\\image0.jpg\"\nfilename=\"static\\uploads\\Classroom of the Elite 2nd Year - Volume 1\\images\\image1.jpg\"\nfilename=\"static\\uploads\\Classroom of the Elite 2nd Year - Volume 1\\images\\image2.jpg\"\nfilename=\"static\\uploads\\Classroom of the Elite 2nd Year - Volume 1\\images\\image3.jpg\""
# , "test23"
# ]

new = []

def sorter(new, data):
    if len(data) <= 0:
        print("\n\nFINISHED...\n\n")
        for i in new:
            print('~~~')
            print(i)
            print('~~~')
        print("Total length: ", len(new))
    else:
        current_position = data[0]
        print(current_position)
        print(current_position.find(a))
        if current_position.find(a) < 0: #Indicates it doesn't exist
            print("Entered 'Else'")
            data.pop()
            sorter(new, data)
        else:
            filenamestring = "filename="
            links = re.findall(filenamestring, current_position)
            print(len(links))
            if len(links) > 1:
                found = current_position.find(a)
                new.append(current_position[:found])
                data[0] = current_position[found:]
                sorter(new, data)
            else:
                new.append(current_position)
                data.pop()
                sorter(new, data)
    sorter(new, data)

def new_sorter(new, data, tag='filename='):
    while len(data) > 0:
        print("CURRENT DATA: ", data)
        curr = data[0]
        print(f"\nCurrently searching in: \n{curr}")
        if curr.find(tag) < 0:
            print("Entered")
            new.append(curr)
            data.pop()
        else:
            links = re.findall(tag, curr)
            print("Number of links: ", len(links))
            if len(links) > 1: #If more than one link
                print("Hi")
                print(f"Original: \n~~~\n{curr}\n~~~")
                print("=============")
                found = curr.find(tag)
                new.append(curr[:curr.find("\n", found)]) #Appends everything up to the thing
                data[0] = curr[curr.find("\n", found):] #Data is now 
                print("=====>>>=======")
                print(f"New: \n~~~\n{data[0]}\n~~~")
            else:   #Only 1 link
                print("Bye")
                print(curr)
                new.append(curr)
                data.pop(0)
                print("NEW DATA: ", data)
    print(len(new))
    for i in new: print(i)

# new = []
# new_sorter(new = new, data=data, tag = 'filename=')

# data =  [[], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image0.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image1.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image2.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image3.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image4.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image5.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image6.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image7.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image8.jpg', 'uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image9.jpg'], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image10.jpg'], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image11.jpg'], [], [], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image12.jpg'], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image13.jpg'], [], [], [], [], [], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image14.jpg'], [], [], [], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image15.jpg'], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image16.jpg'], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image17.jpg'], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image18.jpg'], [], [], [], [], [], [], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image19.jpg'], [], ['uploads\\Classroom of the Elite - Volume 01 [Seven Seas][Kobo]\\images\\image20.jpg']]

# print(data[1][0])

from ebooklib import epub

book = epub.read_epub("book.epub")

# items = book.get_items_of_media_type('image/jpg')

# for item in book.get_items():
#     if item.get_type() == ebooklib.ITEM_DOCUMENT:
#         print('==================================')
#         print('NAME : ', item.get_name())
#         print('----------------------------------')
#         print(item.get_content())
#         print('==================================')


# for index, image in enumerate(book.get_items_of_type(ebooklib.ITEM_IMAGE)):
#         with open(f"test/image{index}.jpg",'wb') as f:
#             f.write(epub.EpubImage.get_content(image))

# images = book.get_items_of_type(ebooklib.ITEM_IMAGE)
# for i in images:
#     print(i)


images = list(book.get_items_of_type(ebooklib.ITEM_IMAGE))

# for index, i in enumerate(book.get_items()):
#         print(i)

class ePubImage:
    def get_name(self):
        return self.file_name

data = []

for index1, file_type in enumerate(book.get_items()): #Gets in proper order
    if type(file_type) == epub.EpubImage:
        for index2, image in enumerate(book.get_items_of_type(ebooklib.ITEM_IMAGE)):
            if file_type == image:
                data.append(image.get_name())

import os  
     
path = 'test/Images'
files = os.listdir(path)
index=0

#TODO: Renaming of files in proper order

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

sort_nicely(data)

for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
    print(image.get_name())

for index, image_name in enumerate(data):
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        if image_name == image.get_name():
            # print(f"Image{index}: {image.get_name()}")
            with open(f"test/image{index}.jpg",'wb') as f:
                    f.write(epub.EpubImage.get_content(image))