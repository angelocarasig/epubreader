# Changelog

### 12/12/2021
* Start
* Many tears are ready to be shed

### 13/12/2021
* EPUB scraping text properly
* GET/POST requests working
* Chapters currently unseperated - Chapters belong in a single list, but can display each chapter's contents on a single web page with some line seperation. Empty chapters containing a single \n still an issue.

### 14/12/2021
* EPUBConverter purges white space accordingly
* Fixed multiple spaces issue when converting epub
* Added folder seperation for each book uploaded, will branch to add images for future image support
* Started working on image support per chapter. 2 main issues:
    - When the file location is passed into the html template, it isn't recognized (smth about percentage signs instead of other symbols) but if replaced in the browser with the correct value, the image loads. so like idk lol
    - Currently only assumes a single image per section (ebooks have multiple chapters, but are not necessarily split accordingly, there can be chapter 8.1, 8.2, 8.3, etc.)

### 15/12/2021 AT 1AM
* holy shit the images are working, idk how it worked but im assuming:
    - brackets in proper direction (??? probs not but still idk haven't tested yet)
    - ensuring correct path location
    - ~~have 20 tabs open at the same time~~
* iteration for each image within the html page

### 15/12/2021
* Cleaned up code
* Moved flasktest.py to app.py
* Proper redirection to reading book and support for going back to home page