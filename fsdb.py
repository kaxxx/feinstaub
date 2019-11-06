#!/usr/bin/python2.7 -u
# coding=utf-8
import datetime

import mysql.connector
import time, json


class Fsdb:

    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                             database='feinstaub',
                                                             user='feinstaub',
                                                             password='feinstaub')

        self.mycursor = self.connection.cursor()

    def write(self, ppm10, ppm2_5):
        try:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            mySql_insert_query = "INSERT INTO readings (time, ppm10, ppm2_5) VALUES (%s, %s, %s)"
            values = [now, ppm10, ppm2_5];
            cursor = self.connection.cursor()
            result = cursor.execute(mySql_insert_query, values)
            self.connection.commit()
            print("Record inserted successfully into readings table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into readings table {}".format(error))

    def writeTime(self, ppm10, ppm2_5, time):
        try:
            # now = time.strftime('%Y-%m-%d %H:%M:%S')
            mySql_insert_query = "INSERT INTO readings (time, ppm10, ppm2_5) VALUES (%s, %s, %s)"
            values = [time, ppm10, ppm2_5];
            cursor = self.connection.cursor()
            result = cursor.execute(mySql_insert_query, values)
            self.connection.commit()
            print("Record inserted successfully into readings table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into readings table {}".format(error))

    def hasTime(self, searchtime):
        # global connection
        #print (self.connection)
        try:
            # "%Y-%m-%d %H:%M:%S:
            checktime = time.strptime(searchtime, '%Y-%m-%d %H:%M:%S')
        except:
            print ("cannot parse timestamp: " + searchtime)
            return True

        try:
            sql = "SELECT * FROM readings WHERE time =  %s"
            adr = (checktime,)

            self.mycursor.execute(sql, adr)
            myresult = self.mycursor.fetchall()

            if len(myresult) == 0:
                return False

            for x in myresult:
               # print "" + str(x[1]) + " = " + str(searchtime) + " ?"

                if str(searchtime) == str(x[1]):
                    print(x)
                    return True
                else:
                    return False

        except mysql.connector.Error as error:
            print("Failed to read readings table {}".format(error))

    def lastTime(self):
        try:
            sql = "SELECT max(time) FROM readings"
            rows_count = self.mycursor.execute(sql)
            myresult = self.mycursor.fetchall()
            if rows_count is not None:
                return datetime.date(2000, 1, 1)
            else:
                return myresult[0][0]
        except:
            print ("error finding last timestamp")

    def getLastDays(self, days):
        xdate = datetime.datetime.now() - datetime.timedelta(days=int(days))
        print "von: "+str(datetime.datetime.now())

        data_ppm = {}
        data_ppm['meta']=[]

        try:
            sql = "select * from readings where time between %s AND now();"
            startdate = (xdate.strftime("%Y-%m-%d %H:%M:%S"),)
            print "bis: " + str(xdate)
            self.mycursor.execute(sql,startdate)
            myresult = self.mycursor.fetchall()
            data_ppm['meta'].append({'from': str(xdate.strftime("%Y-%m-%d %H:%M:%S")), 'to': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),'results':str(self.mycursor.rowcount)})
            for x in myresult:
                dkey = x[1].strftime("%Y-%m-%d %H:%M:%S")
                data_ppm[dkey]=[]
                data_ppm[dkey].append({
                    'ppm10': x[2],
                    'ppm25': x[3]
                })

        except mysql.connector.Error as error:
            print "error finding data in db: {}".format(error)

        return data_ppm

    def __del__(self):
        self.connection.close()

#db = Fsdb()
#db.getLastDays(22)
# db.write(1.1,2.2)
#print (db.hasTime("2018-06-06 11:41:02"))
#ckdate = datetime.strptime("2018-06-06 11:41:02", "%Y-%m-%d %H:%M:%S")
#print (db.lastTime())
#print ckdate
#print ckdate < db.lastTime()
