from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 
import pytz
import logging
logging.basicConfig()


def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)


def get_next_run_time(is_refresh_run):
    now = datetime.now(TZ)
    hour=random.randint(hour_start,hour_end)
    minute=random.randint(minute_start,minute_end)

    if( is_refresh_run ):
        #year = now.year
        #month = now.month
        #day = now.day
        #next_run_time_ = datetime(year,month,day,hour,minute,tzinfo=TZ)
        next_run_time_ = now
    else:
        start_time = datetime(now.year,now.month,now.day,hour_start,minute_start,tzinfo=TZ)
        end_time = datetime(now.year,now.month,now.day,hour_end,minute_end,tzinfo=TZ)
    
        print("next_run_time: %s" % next_run_time)
        print("start_time: %s" % start_time)
        print("end_time: %s" % end_time)
        if start_time <= next_run_time <= end_time:
            print("next_run_time in between")
            next_run_time_ = next_run_time + timedelta(minutes=in_between_delay_minute)
        elif next_run_time < start_time:
            print("next_run_time < start_time")
            next_run_time_ = next_run_time.replace(hour=hour,minute=minute)
        else:
            print("next_run_time > end_time")
            next_run_time_ = next_run_time + timedelta(days=1)
            next_run_time_ = next_run_time_.replace(hour=hour,minute=minute)

    return next_run_time_


hour_start = 2
hour_end = 5
minute_start = 0
minute_end = 59
in_between_delay_minute = 5
scrapy_time = 30 # minute
next_check_hours = 20

TZ=pytz.timezone("Asia/Taipei")
next_run_time = get_next_run_time(True)

sched = BackgroundScheduler(timezone=TZ)
sched.start()


while True:
    jobs=sched.get_jobs()

    if( len(jobs) < 1 ):
        job = sched.add_job(scheduled_job, next_run_time=get_next_run_time(False))
        print "new job scheduled at time: %s" % job.next_run_time
    
    now = datetime.now(TZ)
    time_diff = job.next_run_time + timedelta(hours=next_check_hours) 
    sleep_seconds = next_check_hours * 60 * 60
    print("next check time: %s" % time_diff)
    sleep(sleep_seconds)
