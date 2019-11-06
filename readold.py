#!/usr/bin/python2.7 -u
# coding=utf-8
from datetime import datetime

from fsdb import Fsdb
import time

# db = Fsdb()
# db.write(0.9,0.1)

fppm10 = open('etc/ppm10.txt', 'r')

def ckTime(searchTime, haveTime):
    try:
        searchDate = time.strptime(searchTime, "%Y-%m-%d %H:%M:%S:")
        raw_input()

        haveDate = time.strptime(haveTime, "%Y-%m-%d %H:%M:%S:")
        raw_input()
    except:
        return False;

    if searchDate > haveDate:
        return False
    else:
        return True


def find25(p10time, p10val):
    fppm25 = open('etc/ppm25.txt', 'r')
    line25 = fppm25.readline()
    while line25:
        sp_25 = line25.split(" ")
        if len(sp_25) != 3:
            line25 = fppm25.readline()
            continue
        # try:
        sp25d = sp_25[0]
        sp25t = sp_25[1]
        sp25v = sp_25[2]
        sp25time = sp25d + " " + sp25t
        if sp25time == sp10time:
            print ("Value for " + p10time + " is: " + sp25v)
            return sp25v

        line25 = fppm25.readline()

    fppm25.close()


db = Fsdb()
lasttime = db.lastTime()

line10 = fppm10.readline()
print(line10)

while line10:
    sp_10 = line10.split(" ")
    print("sp10: " + str(sp_10))
    if len(sp_10) != 3:
        line10 = fppm10.readline()
        continue
    sp10time = ""
    sp25v = ""
    sp10v = ""
    # try:
    sp10d = sp_10[0]
    sp10t = sp_10[1]
    sp10v = sp_10[2]
    sp10time = sp10d + " " + sp10t

    try:
        ckdate = datetime.strptime(sp10time, "%Y-%m-%d %H:%M:%S:")
    except:
        print "date parse error"
        line10 = fppm10.readline()
        continue

    #print len(lasttime)
    print "ckdate:"+str(ckdate)
    print "lasttime: "+str(lasttime)
    if lasttime is not None and lasttime > ckdate:
        print "timestamp " + sp10time[:19] + " time is allready in db. continue ..."
        line10 = fppm10.readline()
        continue

    sp25v = find25(sp10time, sp10v)

    line10 = fppm10.readline()

    try:
        db.writeTime(sp10v.strip(), sp25v.strip(), sp10time[:19])
    except:
        print ("no need to write to db!")

fppm10.close()
