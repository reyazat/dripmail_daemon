#!/usr/bin/python
import sqlite3

class NextDrip(object):
	def __init__(self,next_drip_cur):
		self.db = sqlite3.connect(':memory:')
		self.cursor = db.cursor()
		self.__init_db()
		self.__populate_db(next_drip_cur)

	def __init_db(self):
		self.cursor.execute('''CREATE TABLE next_drip_action (
			week_no INTEGER,
			drip_action VARCHAR(20),
			num_visit INTEGER,
			num_click INTEGER,
			subscribe INTEGER,
			next_drip VARCHAR(1))''')

	def __populate_db(self,next_drip_cur):
		cur.executemany('''
			INSERT INTO next_drip_action (week_no, drip_action, num_visit, num_click, subscribe,next_drip)
			VALUES (?,?,?,?,?,?)''',next_drip_cur)
		
	def decide(week_no,drip_action,num_visit,num_click,subscribe):
		self.cursor.execute('''
			SELECT next_drip FROM next_drip_action WHERE week_no = ? AND drip_action = ?
			AND num_visit
			
					  ''')