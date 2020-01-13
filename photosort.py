#!/usr/bin/env python3
import mimetypes
from PIL import Image
import os
import time, datetime
import re
from dateutil import parser
import sys
import glob

version = '0.0.1'

class photosort():

    def __init__(self, argv):
        path = os.path.expanduser(sys.argv[1:][0])
        file_list = self.get_file_list(path)
        print('Number of Images and Videos:', len(file_list))
        
    def get_file_list(self, input_folder):  
        file_list = []     
        files = glob.glob(input_folder + '**', recursive=True)
        
        if files:
            
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
                            date_time = os.path.getmtime(file)
                            #print(datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y"))
                            #date_time = parser.parse(datetime.datetime.fromtimestamp(os.path.getmtime(file)), fuzzy=True, yearfirst=True, ignoretz=True)
                        
                        #create list
                        file_list.append([date_time, file])
                        
        return file_list
                        
        
 

if __name__ == '__main__':
    try:
        photosort(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
