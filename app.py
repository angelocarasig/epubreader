from flask import Flask, render_template, request, url_for, redirect
import os, atexit, shutil
import ePUBConverter, webbrowser, random, threading
from pathlib import Path

app = Flask(__name__, template_folder = "templates")

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
        return redirect(url_for("reader", title = epub_file.filename, path = file_directory))
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


@app.route("/reader", methods=["GET", "POST"])
def reader():
    novel_title = request.args.get('title')
    epub_location = request.args.get('path')
    epub_location_folder = epub_location[:epub_location.rfind("\\")]
    
    generate_images(epub_location, epub_location_folder)
    novel_text = ePUBConverter.convert(epub_location)
    
    
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