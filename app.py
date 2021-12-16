from flask import Flask, render_template, request, url_for, redirect
import os
import ePUBConverter
from pathlib import Path

app = Flask(__name__, template_folder = "templates")

@app.route("/")
def main():
    return redirect(url_for("home"))

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method=="POST":
        epub_file = request.files["file"]        
        
        #Generates a directory for the epub file (to store file + images)
        dirname = os.path.dirname(os.path.abspath(__file__))

        static_folder = dirname + "\\static"
        Path(static_folder).mkdir(parents=True, exist_ok=True)
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


def generate_images(epub_location, epub_location_folder):
    try:
        epub_location_folder += "\\images"
        Path(epub_location_folder).mkdir(parents=True, exist_ok=True)   #Creates images folder

        ePUBConverter.image_support(epub_location)  #Generates the images inside the images folder
    except:
        print("Image collection error. Maybe no images exist for this ePUB?")

def get_images(epub_location):
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


if __name__ == "__main__":
    app.run()