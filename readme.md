#Photorganizer

Photorganizer is a simple command line tool written in python to help you to organize you pictures.

## What it does
You need an input and an output directory. It collects all files in the input directory (including sub folders) and copies them to the output directory according to the following structure:
```
output_directory/year/month/YYYY-mm-dd_HH-MM-SS.ext
```
And `ext` can be any extension of an image or a video (e.g. `.jpg`, `.avi`).

During the process it checks if the target file already exists. Same files will be ignored. If the file differs it copies with a small hash before the extension:
```
output_directory/year/month/YYYY-mm-dd_HH-MM-SS-HASH.ext
```

## What it uses
It uses the DateTimeOriginal EXIF tag to get the date when the image was created. If the tag is not available it uses the last modification date.

## How to use
Copy `photorganizer.py` to directory of your choice. Check if it is executable. 
```
$ ./photorganizer.py input_directory output_directory
$ ./photorganizer.py /home/me/picture_mess/ /home/me/pictures_organized_by_date/
```
