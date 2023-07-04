#!/usr/bin/python
import os
import sys

CURRENT_DIR = os.path.dirname(__file__).replace('\\','/')
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)
	
import dripmail
from daemonize.daemon import Daemon
import datetime,time

class DripMailDaemon(Daemon):		
	def run(self):
		#try:				
		while True:
			f = open('/tmp/DripMailDaemon.txt','w')
			f.write("%s\tdaemon run\n" %(datetime.datetime.now()))
			db = dripmail.ActDB(self.fetch_rec_count,f)			
			f.write("%s\tdaemon started\n" %(datetime.datetime.now()))
			f.flush()
			f.write("%s\tdaemon run defore db.Act\n" %(datetime.datetime.now()))
			db.Act()
			f.write("%s\tdaemon run after db.Act\n" %(datetime.datetime.now()))
			f.flush()
			db.close()
			f.write("%s\tdaemon this period run successfully\n" %(datetime.datetime.now()))
			f.close()			
			time.sleep(int(self.period))
			
		#except Exception as e:
			#print e.strerror
			#f.write("%s\t%s\n" %(datetime.datetime.now(),e.strerror))
		#finally:
			#db.close()
			#f.close()
			#f.write("%s\t%s\n" %(datetime.datetime.now(),"finally"))

if __name__ == "__main__":
	daemon = DripMailDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) >= 2:
		if 'start' == sys.argv[1]:
			daemon.period = 100
			daemon.fetch_rec_count = 1000
			if len(sys.argv) == 3:
				daemon.period = sys.argv[2]
			if len(sys.argv) == 4:
				daemon.fetch_rec_count = sys.argv[3]
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart [period in seconds=100] [fetch_rec_count=1000]" % sys.argv[0]
		sys.exit(2)											