#!/usr/bin/python2.7 -u
# coding=utf-8
import datetime

import mysql.connector
import time, json, thread


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
        self.connection.close()

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
        self.connection.close()

    def hasTime(self, searchtime):
        # global connection
        #print (self.connection)
        try:
            # "%Y-%m-%d %H:%M:%S:
            checktime = time.strptime(searchtime, '%Y-%m-%d %H:%M:%S')
        except:
            print ("cannot parse timestamp: " + searchtime)
            self.connection.close()
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
                    self.connection.close()
                    return True
                else:
                    self.connection.close()
                    return False

        except mysql.connector.Error as error:
            self.connection.close()
            print("Failed to read readings table {}".format(error))

    def lastTime(self):
        try:
            sql = "SELECT max(time) FROM readings"
            rows_count = self.mycursor.execute(sql)
            myresult = self.mycursor.fetchall()
            if rows_count is not None:
                self.connection.close()
                return datetime.date(2000, 1, 1)
            else:
                self.connection.close()
                return myresult[0][0]
        except:
            self.connection.close()
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
            data_ppm['meta'].append({'from': str(xdate.strftime("%Y-%m-%d %H:%M:%S")),
                                     'to': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                     'results': str(self.mycursor.rowcount)})
            for x in myresult:
                self.mkjson(x, data_ppm)
                #thread.start_new_thread(self.mkjson, (x, data_ppm, xdate))

        except mysql.connector.Error as error:
            print "error finding data in db: {}".format(error)
        self.connection.close()
        return data_ppm

    def getLastDaysPl(self, days):
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
            data_ppm['meta'] = {'from': str(xdate.strftime("%Y-%m-%d %H:%M:%S")),
                                     'to': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                     'results': str(self.mycursor.rowcount)}
            data_ppm["x10"] = [];
            data_ppm["y10"] = [];

            data_ppm["x25"] = [];
            data_ppm["y25"] = [];

            for x in myresult:
                self.mkjsonPL(x, data_ppm)
                #thread.start_new_thread(self.mkjson, (x, data_ppm, xdate))

        except mysql.connector.Error as error:
            print "error finding data in db: {}".format(error)
        self.connection.close()
        return data_ppm

    def getRangePL(self, dfrom, dto):
        print "von: " + str(dfrom)
        print "bis: " + str(dto)

        data_ppm = {}
        data_ppm['meta'] = []

        try:
            sql = "select * from readings where time between %s AND %s;"
            self.mycursor.execute(sql, (dfrom, dto))
            myresult = self.mycursor.fetchall()
            data_ppm['meta'] = {'from': dfrom.strftime("%d.%m.%Y %H:%M:%S"),
                                'to': dto.strftime("%d.%m.%Y %H:%M:%S"),
                                'results': str(self.mycursor.rowcount)}

            data_ppm["x10"] = [];
            data_ppm["y10"] = [];

            data_ppm["x25"] = [];
            data_ppm["y25"] = [];

            for x in myresult:
                self.mkjsonPL(x, data_ppm)

        except mysql.connector.Error as error:
            print "error finding data in db: {}".format(error)
        self.connection.close()
        return data_ppm

    def getRange(self, dfrom, dto):
        print "von: " + str(dfrom)
        print "bis: " + str(dto)

        data_ppm = []
        #data_ppm['meta'] = []

        try:
            sql = "select * from readings where time between %s AND %s;"
            self.mycursor.execute(sql, (dfrom, dto))
            myresult = self.mycursor.fetchall()
            #data_ppm['meta'].append({'from': str(dfrom.strftime("%Y-%m-%d %H:%M:%S")),
            #                         'to': str(dto.strftime("%Y-%m-%d %H:%M:%S")),
            #                         'results': str(self.mycursor.rowcount)})
            for x in myresult:
                self.mkjson(x, data_ppm)
                #thread.start_new_thread(self.mkjson, (x, data_ppm, xdate))

        except mysql.connector.Error as error:
            print "error finding data in db: {}".format(error)
        self.connection.close()
        return data_ppm

    def mkjson(self, x, data_ppm):
        xtime = x[1].strftime("%Y-%m-%d %H:%M:%S")
        #data_ppm = []
        data_ppm.append({
             'ppm10': x[2],
             'ppm25': x[3],
             'time': xtime
        })
        return data_ppm

    def mkjsonPL(self, x, data_ppm):
        dkey = x[1].strftime("%Y-%m-%d %H:%M:%S")
        #data_ppm[0] = []

        data_ppm["x10"].append(dkey);
        data_ppm["y10"].append(x[2]);

        data_ppm["x25"].append(dkey);
        data_ppm["y25"].append(x[3]);

        return data_ppm

    def __del__(self):
        self.connection.close()

#db = Fsdb()

#dfrom = datetime.datetime.strptime("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#dto = datetime.datetime.strptime("2019-01-02 00:00:00", "%Y-%m-%d %H:%M:%S")
#print(db.getRange(dfrom, dto))

#print(db.getLastDays(22))
# db.write(1.1,2.2)
#print (db.hasTime("2018-06-06 11:41:02"))
#ckdate = datetime.strptime("2018-06-06 11:41:02", "%Y-%m-%d %H:%M:%S")
#print (db.lastTime())
#print ckdate
#print ckdate < db.lastTime()
