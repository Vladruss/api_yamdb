# -*- coding: utf-8 -*-
import csv, sqlite3
class csvrd:
    def csvFile(self,filename):
        self.readFile(filename)
    
    def readFile(self,filename):
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS test000(p1 varchar,p2 varchar,p3 varchar)""")
        filename.encode('utf-8')
        with open(filename) as f:
            reader = csv.reader(f)
            #for row in reader:
                #cur.execute("INSERT INTO test000 VALUES (?,?,?)", row.split("|"))

        conn.commit()
        conn.close()

c = csvrd().csvFile('users.csv')