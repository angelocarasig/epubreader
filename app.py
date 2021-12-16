from flask import Flask, render_template, request, url_for, redirect, session
import os, atexit, shutil
import ePUBConverter, webbrowser, random, threading
from pathlib import Path

app = Flask(__name__, template_folder = "templates")
'''
For session secret key
'''

app.secret_key = "hello"

#TODO:
# Change to be a chapter-by-chapter format. Needs to know if a previous chapter/next chapter exist and a link to said chapter if true.

'''Can have things done on startup before redirected to home'''
@app.route("/")
def main():
    return redirect(url_for("home"))

'''
Home has variables that contain the title and directory for the epub file. 
TODO: Main menu redirect (read README.md 16/12/2021)
'''
@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method=="POST":
        epub_file = request.files["file"]
        
        #Generates a directory for the epub file (to store file + images)
        dirname = os.path.dirname(os.path.abspath(__file__))

        #Create static folder if uncreated
        static_folder = dirname + "\\static"
        Path(static_folder).mkdir(parents=True, exist_ok=True)

        #Uploads folder
        dirname = f"{dirname}\\static\\uploads\\{epub_file.filename[:-5]}" #Directory for file without .epub extension at end
        Path(dirname).mkdir(parents=True, exist_ok=True)

        #Saves epub to directory
        file_directory = os.path.join("static\\uploads", epub_file.filename[:-5])
        file_directory = os.path.join(file_directory, epub_file.filename)
        epub_file.save(file_directory)

        #Jump to reader page
        session["title"] = epub_file.filename
        session["path"] = file_directory
        return redirect(url_for("reader"))
    else:
        return render_template("index.html")

@app.route('/menu', methods=["GET", "POST"])
def menu():
    title = get_session_title()


'''
Functions used in reader
'''
def generate_images(epub_location, epub_location_folder):
    '''
    Collects all images inside epub and places them in the static directory: uploads/(epubfilename)/images
    '''
    try:
        epub_location_folder += "\\images"
        Path(epub_location_folder).mkdir(parents=True, exist_ok=True)   #Creates images folder

        ePUBConverter.image_support(epub_location)  #Generates the images inside the images folder
    except:
        print("Image collection error. Maybe no images exist for this ePUB?")

def get_images(epub_location) -> list:
    '''Stores each images filename in a list and iterates each image into the html page '''
    images_directories = []
    for section in epub_location:
        if section.find("filename=") >= 0:
            section = section.replace("filename\"static\"", "")
            images_directories.append(section[17:-1])

    for index,val in enumerate(images_directories):
        images_directories[index] = val.replace("\\", "/")

    # for i in images_directories: print(i)
    
    return images_directories

def get_session_title():
    '''
    Session gets title of epub file
    '''
    if "title" in session:
        novel_title = session["title"]
        return novel_title
    else:
        return redirect(url_for("home"))

def get_session_path():
    '''
    Session gets epub file path
    '''
    if "path" in session:
        path = session["path"]
        return path
    else:
        return redirect(url_for("home"))

def get_chapter_list(chapters) -> list:
    '''
    Returns a list of 1's and 0's where 1 = a section and 0 = an image.
    Requires the chapters stored as a list (ePUBConverter.convert) and will check each element. 
    Needs to ignore image-only chapters.
    '''
    chapter_list = []
    for i in chapters:
        if i.find("filename=") >= 0:
            chapter_list.append(0)
        else:
            chapter_list.append(1)
    print(chapter_list)
    return chapter_list

def get_chapter_count(chapter_list) -> int:
    '''
    Returns total number of chapters (NOT COUNTING IMAGES)
    '''
    return chapter_list.count(1)

def set_chapters_data(novel_data, chapter_binary_data, total_chapters):
    '''
    Will generate session data for each chapter. Chapters are labelled numerically e.g Chapter1, Chapter2 Chapter3 etc.\n
    Sessions are stored as dictionary data e.g for the novel's title session["title"] = (noveltitle)\n
    Format for the chapter data will be session["ChapterX"] = [[element1], [element2]...[elementN]]\n
    This allows for images to be attached to a chapter (so there are no chapters that contain only pictures)
    '''
    novel_data_temp = novel_data.copy()
    print("NOVEL DATA: ", novel_data_temp[0])
    print("NOVEL DATA AMOUNT: ", len(novel_data_temp))
    
    for i in range(0, total_chapters):
        curr_chapter_data = []
        starting_point = 0
        curr = chapter_binary_data[starting_point]
        
        if curr == 0: #Is image
            while chapter_binary_data[starting_point + 1] == 1: #While next is an image
                section = []
                section.append(novel_data_temp.pop(starting_point))  #Remove from novel_data and add to section
                curr_chapter_data.append(section)               #Add that section to the current chapter's data
                starting_point += 1

        curr = chapter_binary_data[0]                           #If reached here, it is text, add text to chapter data and finish chapter
        curr_chapter_data.append(curr)
        
        session[f"Chapter{i + 1}"] = curr_chapter_data
        novel_data_temp.pop(0)
    
    print("Checking session items")
    for i,j in session.items():
        print(i, end=": ")
        print(j)
        

@app.route("/reader", methods=["GET", "POST"])
def reader():
    novel_title = get_session_title()
    epub_location = get_session_path()

    epub_location_folder = epub_location[:epub_location.rfind("\\")]
    
    generate_images(epub_location, epub_location_folder)
    
    #Below is a list with each index containing the chapter's contents
    #overrides generate_images if hyperlinks to jpg/png art
    novel_text = ePUBConverter.convert(epub_location)

    #
    chapter_binary_data = get_chapter_list(novel_text)
    total_chapters = get_chapter_count(chapter_binary_data)

    print("Novel text list length: ", len(novel_text))
    print("Total chapters: ", total_chapters)

    # set_chapters_data(novel_text, chapter_binary_data, total_chapters)

    image_list = get_images(novel_text)

    return render_template("book.html", title = novel_title[:-5], content = novel_text, images = image_list)


'''
Exit Handler
'''

def delete_uploads():
    uploads_folder = "static\\uploads"
    try:
        shutil.rmtree(uploads_folder)
    except:
        print("There doesn't seem to be an uploads folder...")

def handle_exit() -> None:
    print("Server shutted down...")
    print("Purging uploads folder...")
    delete_uploads()
    return

atexit.register(handle_exit)

if __name__ == "__main__":
    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port = port, debug=False)