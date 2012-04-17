'''
Created on 17-04-2012

@author: Malwin
'''

import urllib
import urllib2
import cookielib
import os
import subprocess
import re
import string
import shutil
import tempfile
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def prepare_path(path):
    filename = ''
    if os.path.isfile(path):
        path, filename = os.path.split(path)
    elif os.path.isdir(path):
        pass
    else:
        raise Exception("Something wrong with path")
    
    new_path = re.sub(r"\\", '/', path)
    
    return new_path, filename

def process(path, filename, cfg_dict):    
    if filename == '':
        img_list = list(make_screen_dir(path, cfg_dict['screen_amount']))  
    else:
        time_list = make_time_list(path, filename, cfg_dict['screen_amount'])
        img_list = make_screen(path, filename, time_list)
    if cfg_dict['upload']:
        opener = imagebam_login(cfg_dict['username'], cfg_dict['password'])
        upload_imagebam(opener, path, img_list, cfg_dict['thumb_size'])
    if cfg_dict['clean']:
        count = 0;
        print 'Performing cleaning. Deleting screenshots.'
        while count < len(img_list):
            pa = path + '/' + img_list[count]
            print 'Deleting directory : {}'.format(pa)
            shutil.rmtree(pa)
            count += 1
        
def make_time_list(path, filename, screen_amount):
    ffmpeg_command = ['ffmpeg', '-i']
    loc = path + os.sep + filename
    loc2 = re.sub(r"\\", '/', loc)
    ffmpeg_command.append(loc2)
    f = tempfile.TemporaryFile('w+b',prefix='tmp')
    p = subprocess.Popen(ffmpeg_command, stdout = f, stderr = f, shell=True)
    p.wait()
    f.seek(0)
    duration = ''
    for line in f.readlines():
        if 'Duration' in line:
            duration = line[line.find(':')+2:line.index(':')+11]
            break 
    f.close()
    os
    h = duration[:2]
    m = duration[3:5]
    s = duration[6:8]
    total_sec = int(h)*3600 + int(m)*60 + int(s)  
    foo = (total_sec / (screen_amount+1))
    time_list = []
    for i in range(1, screen_amount+1):
        time_list.append(foo*i)
    return time_list

def make_screen(path,filename,time_list):
    ff_input = path + '/' + filename
    count = 0
    filename_size = len(filename)
    filename = filename[0:filename_size-4]
    screen_dir = path + '/' + filename + '/'
    if not os.path.exists(screen_dir):
        os.mkdir(screen_dir)
    while count < len(time_list):
        ff_output = screen_dir + filename + '_' + str(count+1) + '.png'
        ffmpeg_command = ['ffmpeg', '-ss', str(time_list[count]), '-i', ff_input, '-vframes', '1', ff_output ]
        p = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.wait()
        print '{}  --- screen at {}s.'.format(filename, time_list[count]) 
        count += 1
    return filename

def make_screen_dir(path, screen_amount):
    file_list = os.listdir(path)
    movie_file_list = []
    for file_name in file_list:
        if file_name.endswith('.mkv'):
            movie_file_list.append(file_name)
    movie_amount = len(movie_file_list)
    count = 0
    screen_dir_list = []
    while count < movie_amount:
        time_list = make_time_list(path,movie_file_list[count], screen_amount)
        screen_dir_list.append(make_screen(path, movie_file_list[count], time_list))
        count += 1
    return screen_dir_list

def upload_imagebam(opener, path, folder_list, thumb_size):
    global url_upload
    f = open('bbcode.txt', 'w')      
    folder_count = len(folder_list)
    count = 0
    while count < folder_count:
        f.write(folder_list[count])
        f.write("\n\n")
        new_path = path + '/' + folder_list[count]
        img_list = os.listdir(new_path)
        count_2 = 0
        while count_2 < len(img_list):
            file_loc = new_path + '/' + img_list[count_2]
            print "Uploading file :", img_list[count_2]
            #some Imagebam upload options
            datagen, headers = multipart_encode({"file[]": open(file_loc,"rb"), "content_type":"0", 
                                            "thumb_size":thumb_size, "thumb_aspect_ratio":"resize"}) 
            request = urllib2.Request(url_upload, datagen, headers)
            s=urllib2.urlopen(request).read()
            #Looking for BB-CODE
            ind_beg=string.find(s,'[URL')
            ind_end=string.find(s,'[/URL]')
            ind_end+=6
            s=s[ind_beg:ind_end]
            #create file with our image bb-code
            f.write(s)
            f.write(' ')
            count_2 += 1
        f.write("\n\n")
        count += 1;
    f.close()

def imagebam_login(username, password):
    global url_login
    login_data = {'action' : '/login', 'nick' : username, 'pw' : password}
    opener=register_openers()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    login_data_encoded = urllib.urlencode(login_data)
    opener.open(url_login, login_data_encoded)
    return opener