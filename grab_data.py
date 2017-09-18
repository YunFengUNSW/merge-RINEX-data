'''
* Author: Yun Feng
* Contact: 0423472617
* email: yunfeng.unsw@gmail.com
*
* test passed in environment: win10, python 3.6
*
* function: downloading RINEX format data, using the tool 'teqc' to merge multiple files into one
*           multiple files could be within 1 day or across multiple days

* results are saved in the same path of this code
* 
* have fun!
*
'''
import urllib
import os
import datetime
import sys
import gzip  
from pip import download

print(os.path.dirname(sys.argv[0]))
os.chdir(os.path.dirname(sys.argv[0]))

file_list_name = 'tmp_file_list.txt'
root_url = 'ftp://www.ngs.noaa.gov/cors/rinex/'

def un_gz(file_name):  
    f_name = file_name.replace(".gz", "")   
    g_file = gzip.GzipFile(file_name)   
    open(f_name, "wb").write(g_file.read())  
    g_file.close()  

def list_files(url):
    file_list = list()
    urllib.request.urlretrieve(url, file_list_name)
    f = open(file_list_name)
    for row in f:
        file_list.append(row.split(' ')[-1].strip())
    return file_list



if __name__ == '__main__':
    
    #print(len(sys.argv))
    if(len(sys.argv) < 4):
        print('invalid input...')
        print('input format: python3 grab_data nybp start_time end_time')
        print('example: python3 grab_data nybp 2017-09-14T23:11:22Z 2017-09-15T01:33:44Z')
    BS_ID = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    
    save_file_name = str(BS_ID) + '_' +str(start_time.split('T')[0]) + '_'+str(end_time.split('T')[0]) + '.obs'
    if(len(sys.argv) == 5):
       save_file_name = sys.argv[4]

    #BS_ID = 'pbch'
    #start_time = '2017-09-14T23:11:22Z'
    #end_time = '2017-09-15T01:33:44Z'
    
    
    downloaded_files = list()
    my_start_time = ''
    my_end_time = ''
    error = 0
    try:
        my_start_time = datetime.datetime.strptime(str(start_time).upper(),"%Y-%m-%dT%H:%M:%SZ" )
        my_end_time = datetime.datetime.strptime(str(end_time).upper(),"%Y-%m-%dT%H:%M:%SZ" )
    except:
        error = 1
        print('invalid start time format')
        print('time format should be as ISO8601 strings')
        print('for example: 2017-09-14T23:11:22Z')
    
    if error == 0:
        
        if(my_start_time > my_end_time):
            print("position of start_time and end_time maybe wrong, system is trying the reverse way...")
            tmp = my_start_time 
            my_start_time = my_end_time
            my_end_time = tmp
        start_year = my_start_time.year
        end_year = my_end_time.year
        
        if(start_year == end_year):

            url = root_url
            l_year = list_files(root_url)
            if str(start_year) in l_year:
                url = root_url + str(start_year)
                l_day = list_files(url)
                start_nst_day = (my_start_time - datetime.datetime.strptime(str(start_year) + '-01-01T00:00:00Z',"%Y-%m-%dT%H:%M:%SZ" )).days + 1
                end_nst_day = (my_end_time - datetime.datetime.strptime(str(end_year) + '-01-01T00:00:00Z',"%Y-%m-%dT%H:%M:%SZ" )).days + 1
                print("trying to download " + str(end_nst_day - start_nst_day + 1) + "days' rinex data")
                if(end_nst_day - start_nst_day + 1 >= 5):
                    print("warning, files to be downloaded are too many, which would spend too much time")
                    print("press ctrl + c to interrupt if you want to narrow down target files")
                for nst_day in range(start_nst_day, end_nst_day+1):
                    nst_day = str(nst_day)
                    while len(nst_day) < 3:
                        nst_day = '0' + nst_day
                    if nst_day in l_day:
                        url =  root_url + str(start_year) + '/' + nst_day
                        l_bs_id = list_files(url)
                        if str(BS_ID) in l_bs_id:
                            url =  root_url + str(start_year) + '/' + nst_day + '/' + str(BS_ID)
                            l_file = list_files(url)
                            for filename in l_file:
                                hour_of_file = filename.split('.')[0][-1]
                                #print(hour_of_file)
                                is_to_download = True
                                if filename.lower().find('md5') != -1 or filename.lower().find('.gz') == -1:
                                    is_to_download = False
                                if(is_to_download and int(nst_day) == int(end_nst_day)):
                                    if(hour_of_file != '0'):
                                        end_hour_letter = chr(97 + my_end_time.hour)
                                        file_hour_letter = hour_of_file[2].lower()
                                        if(file_hour_letter > end_hour_letter):
                                            is_to_download = False
                                if is_to_download:
                                    url =  root_url + str(start_year) + '/' + nst_day + '/' + str(BS_ID) + '/' + filename
                                    print("downloading the " + str(int(nst_day) - int(start_nst_day) + 1) + ' day\'s file: ' + filename) 
                                    urllib.request.urlretrieve(url, filename)
                                    downloaded_files.append(filename)
                        else:
                            print("invalid Base Station ID...")
            else:
                print("invalid year or data of year " + start_year + "not found")
                
    if len(downloaded_files) > 0:
        print(str(len(downloaded_files)) + " files have been downloaded, marging now..")
        for f in downloaded_files:
            if len(f.split('.')) == 3:
                un_gz(f)
                if (os.path.exists(f) and not os.path.exists(f.replace('.gz', ''))):
                    os.system('gzip -d ' + f)
                print("file " + f + ' uncompressed')
        
        #print(('teqc > ' + ' '.join(downloaded_files).replace('.gz', '') + ' > ' + str(BS_ID) + '_' +str(start_time.split('T')[0]) + '_'+str(end_time.split('T')[0]) + '.obs'))
        print("marging...")
        os.system('teqc > ' + ' '.join(downloaded_files).replace('.gz', '') + ' > ' + save_file_name)
        os.remove(file_list_name)
        for f in downloaded_files:
            if (os.path.exists(f)):
                os.remove(f)
            if (os.path.exists(f.replace('.gz', ''))):
                os.remove(f.replace('.gz', ''))
        print("congratulations, all done")
        
    else:
        print("no valid data found")


  
