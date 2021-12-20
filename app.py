from flask import Flask, render_template, request, url_for, redirect, session
import os, atexit, shutil, json
import ePUBConverter, webbrowser, random, threading
from pathlib import Path

app = Flask(__name__, template_folder = "templates")
SESSION_TYPE = 'filesystem'
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
        return redirect(url_for("menu"))
    else:
        return render_template("index.html")

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

def store_imagetitles_in_list(epub_location) -> list:
    '''Stores each images filename in a list and iterates each image into the html page. No values are added/deleted, only replaced.'''
    images_directories = []

    for section in epub_location.values():
        '''
        Each 'section' is a list item
        '''
        curr_chapter = []
        for i in section:
            if i.find("filename=") >= 0:
                curr_chapter.append(i[i.find("uploads\\"):i.find("\"", i.find("uploads\\"))])
        images_directories.append(curr_chapter)
    
    for section in images_directories:
        for index,val in enumerate(section):
            section[index] = val.replace("\\", "/")
    
    print("Image Directories: \n", images_directories)
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

def set_chapters_data(novel_data) -> dict:
    '''
    Will generate session data for each chapter. Chapters are labelled numerically e.g Chapter1, Chapter2 Chapter3 etc.\n
    Sessions are stored as dictionary data e.g for the novel's title session["title"] = (noveltitle)\n
    Format for the chapter data will be session["ChapterX"] = [[element1], [element2]...[elementN]]\n
    This allows for images to be attached to a chapter (so there are no chapters that contain only pictures)
    '''
    novel_data_temp = novel_data.copy()
    print("NOVEL DATA: \n", novel_data_temp[0])
    print("NOVEL DATA LENGTH: ", len(novel_data_temp))

    curr_chapter = []
    count = 1
    chapters = dict()
    while len(novel_data_temp) > 0:
        curr_selected = novel_data_temp[0]

        if curr_selected.find("filename=") >= 0: #If image
            curr_chapter.append(curr_selected)
            novel_data_temp.pop(0)
        else:
            curr_chapter.append(curr_selected)
            novel_data_temp.pop(0)
            chapters[f"Chapter {count}"] = curr_chapter
            count += 1
            curr_chapter = []
    j = json.dumps(chapters)
    with open("chapters.json", "w") as f:
        f.write(j)
    return chapters
    

@app.route("/menu", methods=["GET", "POST"])
def menu():
    novel_title = get_session_title()
    epub_location = get_session_path()

    epub_location_folder = epub_location[:epub_location.rfind("\\")]
    
    generate_images(epub_location, epub_location_folder)
    
    #Below is a list with each index containing the chapter's contents
    #overrides generate_images if hyperlinks to jpg/png art
    novel_text = ePUBConverter.convert_epub(epub_location)

    dictionary_data = set_chapters_data(novel_text)

    image_list = store_imagetitles_in_list(dictionary_data)
    session['image_list'] = image_list
    session['current_pos'] = 1      #I don't think this is used
    total_chapters = session['total_chapters'] = len(dictionary_data.keys())
    return render_template("book_mainpage.html", title=novel_title[:-5], total_chapters = total_chapters)

@app.route("/reader", methods = ["GET", "POST"])
def reader():
    title = get_session_title()

    chapters = json.load(open("chapters.json"))
    current_pos = int(request.args.get('chapter'))
    image_list = session['image_list']

    try: 
        content = chapters[f'Chapter {current_pos}']
    except:
        print(f"Chapter {current_pos} does not exist! Returning to home page.")
        return redirect(url_for("menu"))

    next = current_pos + 1
    prev=  current_pos - 1

    return render_template("book.html", title = title, content = content, images = image_list, current_image_loc = current_pos - 1, next = next, prev = prev)
    #For some reason jinja can't process ints so we need to make a current, next and prev variable | current_image_loc because chapters start at 1 while the indexes of a list start at 0

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



if __name__ == "__main__":
    port = 5000 + random.randint(0, 999)
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port = port, debug=False)

    atexit.register(handle_exit)