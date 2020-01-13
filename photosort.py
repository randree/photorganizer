#!/usr/bin/env python3
import mimetypes
from PIL import Image
import os
import datetime
import shutil
import re
from dateutil import parser
import sys
import glob
import hashlib

version = '0.0.1'

class photosort():

    def __init__(self, input_path, output_path):
    
        input_path = os.path.join(os.path.abspath(os.path.expanduser(input_path)), '')        
        output_path = os.path.join(os.path.abspath(os.path.expanduser(output_path)), '')
        
        file_list = self.get_file_list(input_path)
        print('Number of Images and Videos:', len(file_list))
        print('Input path:', input_path)
        print('Output path:', output_path)
        
        self.copy_files(file_list, output_path)
        
    def get_file_list(self, input_folder):  
        file_list = []     
        print(input_folder)
        files = glob.glob(input_folder + '**', recursive=True)
        
        if not files:
            return []
            
        for file in files:
            
            date_time = None
            
            if os.path.isfile(file):
                #print(imghdr.what(filename))
                pattern = re.compile('^(image/.+|video/.+)$')
                mime_type = mimetypes.guess_type(file)
                if mime_type[0] and pattern.match(mime_type[0]):
                    #print(mimetypes.guess_type(file))
                    try:
                        exif_date = Image.open(file).getexif()[36867]
                        if exif_date:
                            exif_date = exif_date.replace(":",".", 2)
                        date_time = parser.parse(exif_date, fuzzy=True, yearfirst=True, ignoretz=True)
                        #print(type(date_time))
                        #date = time.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
                        
                    except:
                        date_time = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                        #print(datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y"))
                        #date_time = parser.parse(datetime.datetime.fromtimestamp(os.path.getmtime(file)), fuzzy=True, yearfirst=True, ignoretz=True)
                    
                    #create list
                    file_list.append([date_time, file])
                        
        return file_list
    
    def checksum(self, file):
        #https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
        md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                md5.update(chunk)
        return md5.hexdigest()
                        
        
    def copy_files(self, file_list, output_path):

        for date_time, input_file in file_list:
            filename, file_extension = os.path.splitext(input_file)
            dest_file = os.path.join(
                    output_path, 
                    date_time.strftime("%Y"), 
                    date_time.strftime("%m"),
                    date_time.strftime("%Y.%m.%d_%H:%M:%S") + file_extension.lower())
            
            #check if there is a dest_file already
            if os.path.isfile(dest_file):
                if self.checksum(dest_file) == self.checksum(input_file):
                    print("Skip coping the same file.")
                else:
                    print(input_file, dest_file, "are not identical. Skip coping that file.")
            else:
                try:
                    shutil.copy(input_file, dest_file)
                except IOError as io_err:
                    os.makedirs(os.path.dirname(dest_file))
                    shutil.copy(input_file, dest_file)
                print(input_file, dest_file, "copyed.")


if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            photosort(sys.argv[1], sys.argv[2])
        else:   
            print("You need an input and an output path!")  
    except KeyboardInterrupt:
        sys.exit(0)
