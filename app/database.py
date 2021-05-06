# coding: utf-8
import os
import json
import datetime
from threading import Semaphore

class DB_cl(object):
    def __init__(self, sem):
        self.file_lock = sem

    def read(self, dbfile):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_lock.acquire()
        jsonobject = open(file=current_dir + "/../data/" + dbfile, mode='r', encoding="utf-8")
        result = json.load(jsonobject)
        jsonobject.close()
        self.file_lock.release()
        return result

    def rewrite(self, dbfile, newdata): #Update json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_lock.acquire()
        jsonobject = open(file=current_dir + "/../data/" + dbfile, mode='w', encoding="utf-8")
        json.dump(newdata, jsonobject, indent=4)
        jsonobject.close()
        self.file_lock.release()

    def overwrite(self, dbfile, newdata):  # Update json file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_lock.acquire()
        jsonobject = open(file=current_dir + "/../data/" + dbfile, mode='w', encoding="utf-8")
        json.dump(newdata, jsonobject, indent=4)
        jsonobject.close()
        self.file_lock.release()

    def addwrite(self, dbfile, newdata):  # Update json file
         current_dir = os.path.dirname(os.path.abspath(__file__))
         old=self.read(dbfile)
         old.update(newdata)
         self.file_lock.acquire()
         jsonobject = open(file=current_dir + "/../data/" + dbfile, mode='w', encoding="utf-8")
         json.dump(old, jsonobject, indent=4)
         jsonobject.close()
         self.file_lock.release()

    def update(self,dbfile, key, newdata):
        result = self.read(dbfile)
        result[key] = newdata
        self.overwrite(dbfile,result)

    def create(self, dbfile, newDude, secondKey=None):
        tempfile = self.read(dbfile)
        highest_id=0
        newEntry={}
        for keys in tempfile:
            if int(keys) > highest_id:
                highest_id = int(keys)
        print(highest_id)
        highest_id+=1
        newEntry[str(highest_id)] = newDude
        self.addwrite(dbfile, newEntry)
        return highest_id
