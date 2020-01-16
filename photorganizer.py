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

class photorganizer():

    def __init__(self, input_path, output_path):
    
        input_path = os.path.join(os.path.abspath(os.path.expanduser(input_path)), '')        
        output_path = os.path.join(os.path.abspath(os.path.expanduser(output_path)), '')
        
        file_list = self.get_file_list(input_path)
        print('Number of Images and Videos:', len(file_list))
        print('Input path:', input_path)
        print('Output path:', output_path)
        
        input("Start?")
        
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
                        image = Image.open(file)
                        exif_date = image._getexif()[36867]
                        
                        if not exif_date:
                            raise ValueError("No EXIF date found")
                        
                        #If EXIF string is to short than raise an exeption and take the file timestramp instead
                        if len(exif_date) < 12:
                            raise ValueError("EXIF date string to short")
                            
                        exif_date = exif_date.replace(":",".", 2)
                        date_time = parser.parse(exif_date, fuzzy=True, yearfirst=True, ignoretz=True)  
                        
                    except:
                        date_time = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                    
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
    
    def copy_file(self, input_file, dest_file, i, total):
        try:
            shutil.copy2(input_file, dest_file)
        except IOError as io_err:
            os.makedirs(os.path.realpath(os.path.dirname(dest_file)))
            shutil.copy2(input_file, dest_file)
        print(i, "/", total, input_file, dest_file, "copyed.")
        
                        
        
    def copy_files(self, file_list, output_path):
        
        total = len(file_list)
        i = 0
        
        for date_time, input_file in file_list:
            i += 1
            filename, file_extension = os.path.splitext(input_file)
            dest_file = os.path.join(
                    output_path, 
                    date_time.strftime("%Y"), 
                    date_time.strftime("%m"),
                    date_time.strftime("%Y-%m-%d_%H-%M-%S") + file_extension.lower())
            
            #check if there is a dest_file already
            if os.path.isfile(dest_file):
                hash_input_file = self.checksum(input_file)
                hash_output_file = self.checksum(dest_file)
                if hash_output_file == hash_input_file:
                    print(i, "/", total,"Skip coping the same file.")
                else:
                    dest_file = os.path.join(
                        output_path, 
                        date_time.strftime("%Y"), 
                        date_time.strftime("%m"),
                        date_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + hash_output_file[:3] + file_extension.lower()
                    )
                    self.copy_file(input_file, dest_file, i, total)
            else:
                self.copy_file(input_file, dest_file, i, total)


if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            photorganizer(sys.argv[1], sys.argv[2])
        else:   
            print("You need an input and an output path!")  
    except KeyboardInterrupt:
        sys.exit(0)
