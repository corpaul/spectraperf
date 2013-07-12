'''
Created on Jul 12, 2013

@author: corpaul
'''

import sqlite3
import sys

class InitDatabase(object):
    '''
    classdocs
    '''

    def __init__(self, db):
        '''
        Constructor
        '''
        print "Cleaning database.. %s" % db
        self.con = sqlite3.connect(db)
        with self.con:
            self.createTables()

    def createTables(self):
        cur = self.con.cursor()

        # TODO: add keys
        cur.execute("DROP TABLE IF EXISTS profile")
        cur.execute("DROP TABLE IF EXISTS range")
        cur.execute("DROP TABLE IF EXISTS stacktrace")
        cur.execute("DROP TABLE IF EXISTS type")
        cur.execute("DROP TABLE IF EXISTS monitored_value")
        cur.execute("DROP TABLE IF EXISTS run")

        createProfile = "CREATE TABLE profile ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            revision TEXT NOT NULL, \
                            testcase TEXT NOT NULL);"
        cur.execute(createProfile)

        createRange = "CREATE TABLE range ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            stacktrace_id INTEGER NOT NULL, \
                            min_value INTEGER NOT NULL, \
                            max_value INTEGER NOT NULL, \
                            profile_id INTEGER NOT NULL, \
                            type_id INTEGER NOT NULL);"
        cur.execute(createRange)

        createStacktrace = "CREATE TABLE stacktrace ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            stacktrace TEXT NOT NULL);"
        cur.execute(createStacktrace)

        createStacktrace = "CREATE TABLE type ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            type TEXT NOT NULL);"
        cur.execute(createStacktrace)
        cur.execute("INSERT INTO type (type) VALUES ('BytesWritten')")

        createRun = "CREATE TABLE run ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            revision TEXT NOT NULL, \
                            testcase TEXT NOT NULL);"
        cur.execute(createRun)

        createMonitoredValue = "CREATE TABLE monitored_value ( \
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                            stacktrace_id INTEGER NOT NULL, \
                            value INTEGER NOT NULL, \
                            run_id INTEGER NOT NULL, \
                            type_id INTEGER NOT NULL);"
        cur.execute(createMonitoredValue)

