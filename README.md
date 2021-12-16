# EPUB Reader using Python
Custom EPUB Reader
Built with python 3.9.2 and Flask

Changelog here: [Changelog](Changelog.md)

# Requirements and how to use:
* Must have Python (3.9.2 or newer) and pip installed

1. Clone this repository
2. Open console to the repository's directory
3. Type `pip install -r requirements.txt`
4. Type `app.py`
5. To close press `Ctrl + C` in the console

[Packages](requirements.txt)

# TODO LIST
## Front-End

## Back-End
* ~~Empty Chapters need to be purged~~
* ~~EPUBConverter: Need images to be attached at their respective positions for each chapter~~
* ~~(NEW 15/12/2021): Need everything to be redirected to a new page for the specific novel with back support to go to the starting "submit epub" page~~
* Purging of uploads folder on exit (is this even possible)
* ~~Deploy via Heroku and ensure directories used in code function similarly~~ Staying local indefinitely --> Create an example branch
* Linking webpage CSS
* Chapter Structure - Identification of current chapter and existence of prev/future chapters
* Finding ePUB metadata
* (NEW 16/12/2021): On file upload, redirect to main menu for file. Allow options to start from beginning, start from a specific chapter, view the epub file's contained images and a settings option to control css.