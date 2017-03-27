#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 

#sched = BlockingScheduler()
sched = BackgroundScheduler()


check_period_hr = 20 # hr
scrapy_time     = 5  # minute

job_id="scrapy_job"

#@sched.scheduled_job('cron', id="scrapy_job", hour=3, minute=55)
def scheduled_job():
    cmd = "scrapy crawl visitcount"
    cmd = "ls"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)
    #sleep(check_period_hr*60*60 - 5*60)

sched.start()

while True:
    jobs=sched.get_jobs()

    if( len(jobs) < 1 ):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour=random.randint(18,20)
        minute=random.randint(0,59)
        
        next_run_time = datetime(year,month,day,hour,minute)
            
        job = sched.add_job(scheduled_job,id="scrapy_job",next_run_time=next_run_time)
        #scheduler.reschedule_job('scrapy_job', trigger='cron', hour=hour, minute=minute)
        print "new job scheduled at time: %s" % job.next_run_time
    
    total_sleep = timedelta(seconds=(check_period_hr*60*60 - scrapy_time*60))
    print("sleep now for: %s" % str(total_sleep))
    #sleep(check_period_hr*60*60 - 5*60)
    sleep(5)

#def scheduled_job():
#    cmd = "scrapy crawl visitcount"
#    print('Late night crawler is running: %s' % cmd)
#    subprocess.Popen(cmd, shell=True)


#jobs = sched.get_jobs()
#print(jobs)
#print "xxxxxxxxxxxxx"
