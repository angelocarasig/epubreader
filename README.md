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

[Requirements](requirements.txt)

# Examples:
### Example 19/12/2021:
embedded image links aren't able to be in proper coordination with the raw images inside the epub file. Hence a wait time, the program downloads the images, saves them locally and *then* loads the page. Unconventional but also is a reason why officials are better. No chapter support in this one - everything is loaded into a single page. No front-end work either, just want to get the flask backend working for now.
https://imgur.com/a/KrIHshL

### Example 20/12/2021:
Somewhat functional main menu implemented. Displays total sections, chapters are seperated appropiately, correct images show at their correct positions. Throws user back to main menu when accessing invalid chapter (e.g next chapter on last chapter or entering a large number in browser)
https://imgur.com/a/OkfYIGL

#
# TODO LIST
## Front-End

## Back-End
* ~~Empty Chapters need to be purged~~
* ~~EPUBConverter: Need images to be attached at their respective positions for each chapter~~
* ~~(NEW 15/12/2021): Need everything to be redirected to a new page for the specific novel with back support to go to the starting "submit epub" page~~
* ~~Purging of uploads folder on exit (is this even possible)~~ yes it is
* ~~Deploy via Heroku and ensure directories used in code function similarly~~ Staying local indefinitely --> Create an example branch
* Linking webpage CSS
* ~~Chapter Structure - Identification of current chapter and existence of prev/future chapters~~ ~~If next/prev chapter doesn't exist, throw them back into main menu~~ DONE!
* ~~Finding ePUB metadata~~ Probably impossible --> try to find ToC 
* (NEW 16/12/2021): ~~On file upload, redirect to main menu for file. Allow options to start from beginning~~, start from a specific chapter, view the epub file's contained images and a settings option to control css.
* ~~(NEW 16/12/2021): Read and do changelog 16/12/2021's TODO~~
