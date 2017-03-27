#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 

#sched = BlockingScheduler()
sched = BackgroundScheduler()

sched.start()

check_period_hr = 20 # hr
scrapy_time     = 5  # minute

#@sched.scheduled_job('cron', hour=hour, minute=minute)
def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)
    #sleep(check_period_hr*60*60 - 5*60)

while True:
    jobs = sched.get_jobs()

    if( len(jobs) < 1 ):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour=random.randint(2,6)
        minute=random.randint(0,60)
        
        next_run_time = datetime(year,month,day,hour,minute)
            
        job = sched.add_job(scheduled_job, next_run_time=next_run_time)
        print("job added: %s" % job)
    
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
