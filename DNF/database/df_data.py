#!/usr/bin/python
from datetime import datetime
import sys, os, time
from DNF import conf
from DNF.database.storage import Database

class Data:

    def __init__(self):
        pass


    def getIp4(self, ip4):
        sql = sql = "select * from clients where IP4='%s'" % ip4
        return Database.get_row(sql)


    def active(self, type, search):
	
        if type(search) == str:
		sql = "select Active from clients where %s='%s'" % (type,user)
	else:
		# obs. maa vite type i database
		sql = "select Active from clients where %s={1}" % (type,search) 
		
	active = Database.get_row(sql)[0]

        if active and active == 1:
            return True
        else:
            return False

    def get_info_client(self,get_type,search_type,search):

	if type(search) == str:
	    sql = "select %s from clients where %s='%s'" % (get_type,search_type,search)
        else:
                # obs. maa vite type i database
                sql = "select %s from clients where %s={1}" % (get_type,search_type,search)

                return Database.get_row(sql)[0]

    def DbAddRow(self,user,mac,ip4,ip6):

        #add a new user, or updating an exsiting one


        if len(mac) != 17 and len(ip4) < 7 and len(ip4) > 17:
            raise ValueError("somthing od with ip4/mac")
        elif self.get_info_client("User","IP4",ip4):
            sql = "UPDATE clients set Mac='%s', IP4='%s', IP6='%s', Active=1 WHERE User='%s'" % (mac,ip4,ip6,user) 
        else:
            sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', 1) " % (user,mac,ip4,ip6)
        Database.alter(sql)

    def DbActiveUser(self,user,active):

    #acitvates or deactivates an user
 

        sql = "UPDATE clients SET Active=%s WHERE User='%s'" % (active,user)
            
        Database.alter(sql)

    def DbActiveIp4(self, ip4, active):
        sql ="UPDATE clients SET Active=%i WHERE IP4='%s'" % (active,ip4)
        Database.alter(sql)

    def DbUpdateRow(self,user,data):

    #updates one part in a user`s row

     # maybeh make a better check for it...


        if len(data) > 17:
            type = "IP6"
        elif len(data) == 17:
            type = "Mac"
        elif len(data) > 7:
            type = "IP4"
        else:
            raise ValueError("input error")

        sql = "UPDATE clients SET %s='%s', Active=1 WHERE User='%s'" % (type,data,user)

        Database.alter(sql)
    

    def updateStats(self, user, connections, tx, rx):
    
        sql = "select tx_total, rx_total, UNIX_TIMESTAMP(Time) from stats where User='%s'" % (user)
        row = Database.get_row(sql)    
        if row:
            tx_total = tx + row[0]
            rx_total = rx + row[1]
            sec = int(time.time() - row[2])
            if sec > 0:
                txs = tx_total/sec
                rxs = rx_total/sec
            else:
                txs = 0
                rxs = 0
            sql= "UPDATE stats SET Connections=%i, tx_total=%i, rx_total=%i, txs=%i, rxs=%i, Time=FROM_UNIXTIME(%s) WHERE User='%s'" % (connections,tx_total,rx_total,txs,rxs,time.time(),user) 
            
            
        else:
            Time = time.time()
            sql = "INSERT INTO stats VALUES ('%s', %i, %i, %i, 0, 0,FROM_UNIXTIME(%s))" %(user,connections,tx,rx,Time)

        Database.alter(sql)

    def aboveDownLimit(self, limit):
        sql = "SELECT User FROM stats WHERE rxs > %i" %(limit)
        return Database.get_all_rows(sql)
        
    def aboveUpLimit(self, limit):
        sql = "SELECT User FROM stats WHERE txs > %i" %(limit)
        return Database.get_all_rows(sql)
        
    def aboveConnectionLimit(self, limit):
        sql = "SELECT User FROM stats WHERE Connections > %i" %(limit)
        return Database.get_all_rows(sql)

        
    def topFiveDownload(self):
        sql = "SELECT user, rxs FROM stats ORDER BY rxs DESC LIMIT 5"
        return Database.get_all_rows(sql)

    def topFiveConnections(self):
        sql = "SELECT user, connections FROM stats ORDER BY connections DESC LIMIT 5"
        return Database.get_all_rows(sql)
    
    def topFiveUpload(self):
        sql = "SELECT user, txs FROM stats ORDER BY txs DESC LIMIT 5"
        return Database.get_all_rows(sql)
    
    def highscore(self):
        tx_total = "SELECT user, tx_total FROM stats ORDER BY tx_total DESC LIMIT 1"
        rx_total = "SELECT user, rx_total FROM stats ORDER BY rx_total DESC LIMIT 1"
        txs = "SELECT user, txs FROM stats ORDER BY txs DESC LIMIT 1"
        rxs = "SELECT user, rxs FROM stats ORDER BY rxs DESC LIMIT 1"
        con = "SELECT user, connections FROM stats ORDER BY connections DESC LIMIT 1"
        
        tx_total = Database.get_all_rows(tx_total)
        rx_total = Database.get_all_rows(rx_total)
        txs = Database.get_all_rows(txs)
        rxs = Database.get_all_rows(rxs)
        con = Database.get_all_rows(con)


        return (tx_total, rx_total, txs, rxs, con)
        
