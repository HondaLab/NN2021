#! /usr/bin/python3
import csv
import platform

FILE1 = "/home/pi/2DOVR/parm_smm.csv"
FILE2 = "/home/pi/2DOVR/framesize.csv"

def read_parm(filepath):
    file_p = open(filepath, "r")
    tmp = []
    reader = csv.reader(file_p)
    header = next(reader)
    for row in reader:
        if len(row) == 0:
            pass
        else:
            tmp.append(float(row[0]))
            tmp.append(float(row[1]))
            tmp.append(float(row[2]))
            tmp.append(float(row[3]))
            tmp.append(float(row[4]))
            tmp.append(float(row[5]))
            tmp.append(float(row[6]))
    return tmp

def read_framesize(filepath):
    file_p = open(filepath, "r")
    tmp = []
    reader = csv.reader(file_p)
    header = next(reader)
    for row in reader:
        if len(row) == 0:
            pass
        else:
            tmp.append(row)
    EMAIL_SUBJECT_PREFIX = '[%s]' % platform.uname()[1]
    hostname = EMAIL_SUBJECT_PREFIX.replace("[",'')
    hostname = hostname.replace("]",'')

    print(hostname)
    hostname = hostname.replace('ssr','')
    print(hostname)
    
    for i in range(len(tmp)):
        if hostname == str(tmp[i][0]):
            upper = int(tmp[i][1])
            lower = int(tmp[i][2])
        else:
            #print("該当なし")
            pass    
    return upper,lower


if __name__ == "__main__":
    print(read_parm(FILE1))
    print()
    print(read_framesize(FILE2))
