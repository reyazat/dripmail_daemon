#!/usr/bin/python
import os
import sys
#import json    
from next_drip import NextDrip

CURRENT_DIR = os.path.dirname(__file__).replace('\\','/')
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from mysql import mysql_db as m
from settings import *
import datetime

class ActDB(object):
    def __init__(self,fetch_rec_count=1000,logger=None):
        self.logger = logger
        self.db_mysql = m.DB(DATABASES['default']['NAME'],DATABASES['default']['USER'],DATABASES['default']['PASSWORD']
                                            ,DATABASES['default']['HOST'],int(DATABASES['default']['PORT']), 1)
        self.db_mysql.conn.autocommit(False)

        self.limit = fetch_rec_count
        self.log('ActDB initialized')
        
    def close(self):
        self.db_mysql.close()
        self.log('DB Closed')
        
    def log(self,msg):
        if self.logger is not None:
            self.logger.write("%s %s\n" %(datetime.datetime.now(),msg))
            self.logger.flush()
    
    def search(self, id, list_of_dic):
        return [element for element in list_of_dic if element['id'] == id or element['parent'] == id]
    
    def Act(self):
        self.log('Running ActDB.Act')
        select_robot_status = "SELECT allow,status FROM `om_robot_status` WHERE robotname = 'dripaction'"
        cur_rob_sta = self.db_mysql.execute(select_robot_status)
        sta_rec = cur_rob_sta.fetchone()
        if sta_rec['allow'] != 'Yes':
            self.log('Dripaction is disabled')
            return
        if sta_rec['status'] != 'Waiting':
            self.log('Dripaction is busy')
            return 
        
        update_robot_status = "UPDATE `om_robot_status` SET status = 'Busy' WHERE robotname = 'dripaction'"
        self.db_mysql.execute(update_robot_status)
        self.db_mysql.commit()
        
        next_drip = NextDrip()
        self.log('NextDrip initialized')
        offset = 0
        select_dripaction = '''SELECT id, actionname FROM om_dripaction'''
        cur1 = self.db_mysql.execute(select_dripaction)
        rows1 = cur1.fetchall()        
        dripaction_dic = {}
        for row in rows1:
            dripaction_dic[row['actionname']] = row['id']
        
        self.log('dripaction_dic constrcted')
        print 'before while True'
        while True:
            # -- OR ((es.parent IS NOT NULL or es.parent !=0) AND DATEDIFF(NOW(),esp.senddate) < 28)
            print( 'while True')
            select_ids = '''
                SELECT  es.id, es.parent FROM `om_email_status` es                
                LEFT OUTER JOIN `om_email_status` esp ON es.parent = esp.id
                WHERE es.checked = 0 AND  
                (
                (es.parent <> 0 AND DATEDIFF(NOW(),esp.senddate) < 28 ) OR
                (es.parent = 0 AND DATEDIFF(NOW(),es.senddate) < 28 )
                )
                LIMIT %d,%d            
            '''
            print(select_ids)
            select_ids = select_ids %(offset,self.limit)
            
            self.log(select_ids)

            self.log('Executing select to get ids')
            self.log(select_ids)
            cursor_ids = self.db_mysql.execute(select_ids)
            self.log('Select executed')
            if cursor_ids.rowcount == 0:
                break
                
            self.log('Fetching all ids')    
            rows_ids = cursor_ids.fetchall()
            
            ids = (d['id'] for d in rows_ids)
            parent_ids = (d['parent'] for d in rows_ids)
            all_ids_list = list(set(ids + parent_ids) - set([0]))
            
            all_ids = ','.join( str(d) for d in all_ids_list)
            self.log('all_ids : %s' %(all_ids))
            select_sql = '''
                SELECT  DATEDIFF( NOW( ) , es.senddate) as elapsed_days,
                IFNULL(da.actionname,'main') as actionname,es.* FROM `om_email_status` es
                LEFT OUTER JOIN `om_dripaction` da ON es.iddripaction = da.id
                LEFT OUTER JOIN `om_email_status` esp ON es.parent = esp.id
                WHERE es.id in (%s) or es.parent in (%s)
                order by elapsed_days
            '''
            # select_sql = '''
                # SELECT  IF((es.parent IS NULL OR es.parent = 0),DATEDIFF( NOW( ) , es.senddate ),DATEDIFF( NOW( ) , esp.senddate )) as elapsed_days,
                # IFNULL(da.actionname,'main') as actionname,es.* FROM `om_email_status` es
                # LEFT OUTER JOIN `om_dripaction` da ON es.iddripaction = da.id
                # LEFT OUTER JOIN `om_email_status` esp ON es.parent = esp.id
                # WHERE es.id in (%s) or es.parent in (%s)
                # order by 
            # '''

#            old_select_sql = '''
#                SELECT  IF(es.parent IS NULL,DATEDIFF( NOW( ) , es.senddate ),DATEDIFF( NOW( ) , esp.senddate )) as elapsed_days,
#                IFNULL(da.actionname,'main') as actionname,es.* FROM `om_email_status` es
#                LEFT OUTER JOIN `om_dripaction` da ON es.iddripaction = da.id
#                LEFT OUTER JOIN `om_email_status` esp ON es.parent = esp.id
#                WHERE es.checked = 0 AND ((es.parent IS NOT NULL AND DATEDIFF(NOW(),esp.senddate) < 28)
#                OR (es.parent IS NULL AND DATEDIFF(NOW(),es.senddate) < 28)) LIMIT %d,%d            
#            '''
            
            self.log('Executing select statement')
            self.log(select_sql %(all_ids,all_ids))
            cursor = self.db_mysql.execute(select_sql %(all_ids,all_ids))
            self.log('Select executed')
            if cursor.rowcount == 0:
                break
                
            self.log('Fetching all record')    
            rows = cursor.fetchall()
            self.log('Records fetched')    
            main_ids =  [element for element in rows if (element['parent'] is None or element['parent']== 0)]
            for row in main_ids:
                #now = str(datetime.datetime.now())                
                dict_of_mails =self. search(row['id'], rows)
                f_list = self.__none_to_null(dict_of_mails)
                
                # next_drip_action = next_drip.decide(f_dic['elapsed_days'],f_dic['actionname'],f_dic['numvisit'],f_dic['numclick'],f_dic['subscribe'])
                next_drip_action = next_drip.decide(f_list)
                self.log('Next drip action defined')    
                iddripaction = 0
                if next_drip_action == 'R': iddripaction = dripaction_dic['resend']
                if next_drip_action == 'R': iddripaction = dripaction_dic['resend']
                if next_drip_action == 'F': iddripaction = dripaction_dic['fallowup']
                if next_drip_action == 'E': iddripaction = dripaction_dic['extraincentive']
                if next_drip_action == 'T': iddripaction = dripaction_dic['thankyou']
                
                self.log('Initializing insert...')    
                insert_stmt = "INSERT INTO `om_robot_sender` VALUES (null,%s, %s,%s,%s,'%s',%s,'%s','%s','%s','%s','%s',NOW())" \
                    %(f_list[0]['idowner'],f_list[0]['idmaker'],f_list[0]['iddraft'],iddripaction,f_list[0]['type'],f_list[0]['idgroupmail']
                    ,f_list[0]['subject'],'recepient','from',f_list[0]['senddate'],'COMP')
                
                update_stmt = "UPDATE om_email_status SET checked=1 WHERE id = %s" %(f_list[0]['id'])
                self.log('Executing insert')
                self.log(insert_stmt)
                self.db_mysql.execute(insert_stmt)
                self.log(update_stmt)
                self.db_mysql.execute(update_stmt)
                self.log('Insert executed')    
            offset += self.limit
            self.db_mysql.commit()
            self.log("Commited")
        
        update_robot_status = "UPDATE `om_robot_status` SET status = 'Waiting' WHERE robotname = 'dripaction'"
        self.db_mysql.execute(update_robot_status)
        self.db_mysql.commit()
    def __none_to_null(self,list_of_dic):
        list2 = []
        for dic in list_of_dic:
            dic2 = {}
            for k, v in dic.iteritems():
                if v is None:
                    dic2[k] = 'null'
                else:
                    dic2[k] = v
            list2.append(dic2)
        return list2


    #def __exit__(self):        

if __name__ == "__main__":
    f = open('DripMailLog.txt','w')
    if len(sys.argv) == 2:
        db = ActDB(int(sys.argv[1]),f)
    else:
        print "usage: %s [fetch_rec_count=1000]" % sys.argv[0]
        db = ActDB(1000,f)
    
    db.Act()
    db.close()
    f.close()
    print('Dripmail executed')


