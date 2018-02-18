import os
import csv
import sys
import re
import time
from argparse import ArgumentParser

CSV_HEADER = ['volume','abs_path','depth','drive','directory','filename','extension','is_file','is_dir','is_link','size_in_bytes','creation_time','modify_time']

def create_csv_line(myFileName, volume):

    abs_path = myFileName

    temp_split = re.split(r"\\",abs_path)
    depth = str(len(temp_split)-1)

    drive = os.path.splitdrive(myFileName)[0]
    directory = os.path.split(myFileName)[0] 
    filename = os.path.basename(myFileName)
    extension = os.path.splitext(myFileName)[1].lower()
    is_file = str(os.path.isfile(myFileName))
    is_dir = str(os.path.isdir(myFileName))
    is_link = str(os.path.isdir(myFileName))
    size_in_bytes = str(os.path.getsize(myFileName))
    
    ctime_year = str(time.gmtime(os.path.getctime(myFileName)).tm_year)
    ctime_month = str(time.gmtime(os.path.getctime(myFileName)).tm_mon)
    ctime_day = str(time.gmtime(os.path.getctime(myFileName)).tm_mday)
    creation_time = "-".join([ctime_year,ctime_month,ctime_day])

    mtime_year = str(time.gmtime(os.path.getmtime(myFileName)).tm_year)
    mtime_month = str(time.gmtime(os.path.getmtime(myFileName)).tm_mon)
    mtime_day =  str(time.gmtime(os.path.getmtime(myFileName)).tm_mday)
    modify_time = "-".join([mtime_year,mtime_month,mtime_day])
    
    csv_line = [volume,abs_path,depth,drive,directory,filename,extension,is_file,is_dir,is_link,size_in_bytes,creation_time,modify_time]
    csv_line_clean = []

    for element in csv_line:
        csv_line_clean.append(element.encode('ascii','ignore').decode('UTF-8'))

    return csv_line_clean

def main():

    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", help="Path of the volume/directory to scan", required="True")
    parser.add_argument("-o", "--output", dest="output", help="Output CSV filename", required="True")
    parser.add_argument("-v", "--volume", dest="volume", help="Name of the volume", required="True")
    
    args = parser.parse_args()

    writer = csv.writer(open(args.output,"w"), delimiter=';', lineterminator = "\n")
    writer.writerow(CSV_HEADER)
    
    for dirname, dirnames, filenames in os.walk(args.path):
    # print path to all subdirectories first.
        for subdirname in dirnames:
            myFileName = os.path.join(dirname, subdirname)
            csv_line = create_csv_line(myFileName, args.volume)
            writer.writerow(csv_line)
            print(csv_line)

    # print path to all filenames.
        for filename in filenames:
            myFileName = os.path.join(dirname, filename)
            csv_line = create_csv_line(myFileName, args.volume)
            writer.writerow(csv_line)
            print(csv_line)

if __name__ == "__main__":
    main()
