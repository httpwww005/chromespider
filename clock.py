from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 


def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)


def get_next_run_time(is_refresh_run):
    now = datetime.now()
    hour=random.randint(2,6)
    minute=random.randint(0,59)

    if( is_refresh_run ):
        year = now.year
        month = now.month
        day = now.day
        next_run_time_ = datetime(year,month,day,hour,minute)
    else:
        next_run_time_ = next_run_time + timedelta(days=1)
        next_run_time_ = next_run_time_.replace(hour=hour,minute=minute)

    return next_run_time_


sched = BackgroundScheduler()
next_run_time = get_next_run_time(True)

check_period_hr = 20 # hr
scrapy_time     = 10 # minute


sched.start()


while True:
    jobs=sched.get_jobs()

    if( len(jobs) < 1 ):
        job = sched.add_job(scheduled_job, next_run_time=get_next_run_time(False))
        print "new job scheduled at time: %s" % job.next_run_time
    
    now = datetime.now()
    time_diff = next_run_time - now
    total_sleep = time_diff.total_seconds()
    print("sleep now for: %s" % str(timedelta(seconds=total_sleep)))
    sleep(total_sleep)
