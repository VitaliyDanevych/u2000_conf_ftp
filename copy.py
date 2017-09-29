#!/usr/bin/python2.7 
#  #!/usr/bin/env python
#first
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2015 Kiev, Ukraine'
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


import sys
import re
from ftplib import FTP
import datetime


#define the constants
HOST = '10.XX.XX.101'
USER = 'ftpXXX'
PASSWD = 'angXXX'
TO_COPY_DIR = '/home/na_scripts/u2000_conf_parser/CURRENT/'
LINK_REPORT_FILENAME = 'Microwave_Link_Report.txt'



def connect_ftp(hostname=HOST, username=USER, password=PASSWD):
  '''connect to ftp-server specified in arguments.
  if no arguments specified than uses defaults values from constants
  '''
  global ftp
  #print socket.getdefaulttimeout()
  #print socket.getaddrinfo(hostname, 21)
  #exit(1)
  try:
    ftp = FTP(hostname, timeout=15)
  except: # ftplib.all_errors, e:
    print 'ERROR: cannot reach "%s"' % hostname
    exit(1) # the is no sense in further running this program, exit from it with error code 1 
  print '*** Connected to host "%s"' % hostname
  try:
    ftp.set_pasv(True)
  except:
    print 'ERROR: cannot change ftp mode to passive'
    print "ftp.set_pasv(1)", ftp.set_pasv
  try:
    ftp.login(username, password)
  except: # ftplib.error_perm:
    print 'ERROR: cannot login to server "%s"' % hostname
    exit(1)
  return ftp
 
  
def cwd_ftp_dir(dir):
  """ Enter to the folders, calculates needed further folder and executing a download function"""
  global dirname
  dirname = dir 
  try:
      ftp.cwd(dirname)
  except: # ftplib.error_perm:
      print ('Error changing to ftp directory %s' % dirname)
  print '*** Listed the directory: "%s"' % dirname
    
  if dirname == '/':
      print "You are within of ", ftp.pwd() # nothing doing
      print "I will do nothing"
 
  if dirname == '\script':
      print "You are within of ", ftp.pwd()
      try:
        list_of_items = ftp.nlst()
      except:
        print "An exception occurs during list of ftp dir"
        exit(1)
      max_date, needed_dir_name = get_max_date(dirname, list_of_items) #find the max date at folder
      print needed_dir_name
      try:
        ftp.cwd(needed_dir_name)
      except: # ftplib.error_perm:
        print ('Error changing to ftp directory %s' % needed_dir_name)
      print "You are within of ", ftp.pwd()
      list_of_files = ftp.nlst()
      print "I will download the files from ftp"
      download_from_ftp(dirname, list_of_files, max_date)
      
  if dirname == '\link_report':
      print "You are within of ", ftp.pwd()
      list_of_files = ftp.nlst()
      print "I am going to download the files from ftp"
      download_from_ftp(dirname, list_of_files)
      
          
def download_from_ftp(dirname, list_of_files, max_date=00000000):
  """ for downloading specific files and modifies filenames """
  
  if dirname == '\script':
    index = 0
    for filename in list_of_files:
      mask_match = re.search('NED|NWC', filename)
      if mask_match:
        index += 1
        filename_new = filename.replace('_(UTF-8)', '')
        filename_new = filename_new.replace(' ', '_')
        if mask_match.group() == 'NWC':
          filename_new = filename_new + '_' + str(datetime.datetime.now().strftime("%Y%m%d"))
        ftp.retrbinary('RETR %s' % filename, open(TO_COPY_DIR+filename_new, 'w').write)  #comments this if downloading files is not needed
        print index, "max_date folder:", max_date, "file:", filename, " --> ", TO_COPY_DIR + filename_new, "copied."
        
  if dirname == '\link_report':
    try:
      max_file_date, filename = get_max_date(dirname, list_of_files) #only 1 file is expected
    except:
      print "An error occurs during an execution of get_links_file_max_date function"
    try:
      ftp.retrbinary('RETR %s' % filename, open(TO_COPY_DIR+LINK_REPORT_FILENAME, 'w').write)
    except:
      print "An error occurs during of downloading a %s file" % filename
    print "max_file_date:", max_file_date, "file:", filename, " --> ", TO_COPY_DIR + LINK_REPORT_FILENAME, "copied."
    

def dict_mdate(date_tuple):
  """Function needed for correct sorting and finding the most up-to-date link file in dict from the given files."""
  return date_tuple[0]  
    

def get_max_date(dirname, list_of_items):
  """this function finds the folder within of \script'
  where the max date and returns one this folder"""
  dict_matched = {}
  dict_date = {}
  for each_item in list_of_items:
    if dirname == '\script':
      #to find the most up-to-date folder like as Schedule_20150617_060026
      match = re.match(r'Schedule_', each_item)
      if match:
        dict_matched = re.findall(r'Schedule_(\d\d\d\d)(\d\d)(\d\d)', each_item) ##Schedule_20150617_060026
    elif dirname == '\link_report':
      #to find the most up-to-date file like as Microwave Link Report_06-16-2015_07-17-42.csv
      match = re.match(r'^Micro', each_item)
      if match:
        dict_matched = re.findall(r'Report_(\d+)-(\d+)-(\d+)', each_item) #Microwave Link Report_06-16-2015_07-17-42.csv
    else: print "There are not \script or \link_report ftp folder"
    for item in dict_matched:
      if dirname == '\script':
        date_uniq = datetime.date(int(item[0]), int(item[1]), int(item[2]))
      elif dirname == '\link_report':
        date_uniq = datetime.date(int(item[2]), int(item[0]), int(item[1]))
      else: print "There are not \script or \link_report ftp folder2"
      if date_uniq not in dict_date:
        dict_date[date_uniq] = each_item
  sorted_dict = sorted(dict_date.items(), key=dict_mdate, reverse=True)
  #print sorted_dict[0]
  for item in sorted_dict[:1]:  # Print the first 5 dates
    return item[0], item[1] # this function returns max data and filename/folder with max data as strings
              

def main():
  print "the connect_ftp function has started"
  connect_ftp()
  print "the connect_ftp function has ended"
  
  print "the cwd_ftp_dir function has started"
  cwd_ftp_dir('\script')
  print "the cwd_ftp_dir function has ended"
  
  #print "the cwd_ftp_dir function has started"
  #cwd_ftp_dir('/')
  #print "the cwd_ftp_dir function has ended"
  
  print "the cwd_ftp_dir function has started"
  cwd_ftp_dir('\link_report')
  print "the cwd_ftp_dir function has ended"
  
  ftp.quit()
  
if __name__ == '__main__':
    main()
