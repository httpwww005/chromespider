from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 
import pytz
import logging
logging.basicConfig()


hour_start = 2
hour_end = 5
minute_start = 0
minute_end = 59
in_between_delay_minute = 5
scrapy_time = 30 # minute
next_check_hours = 20

TZ=pytz.timezone("Asia/Taipei")


def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)


def get_next_run_time(is_refresh_run):

    if( is_refresh_run ):
        next_run_time_ = datetime.now(TZ)
    else:
        hour=random.randint(hour_start,hour_end)
        minute=random.randint(minute_start,minute_end)

        start_time = datetime(next_run_time.year,next_run_time.month,next_run_time.day,hour_start,minute_start,tzinfo=TZ)
        end_time = start_time.replace(hour=hour_end, minute=minute_end)
    
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


next_run_time = get_next_run_time(True)

sched = BackgroundScheduler(timezone=TZ)
sched.start()


while True:
    jobs=sched.get_jobs()

    if( len(jobs) < 1 ):
        next_run_time = get_next_run_time(False)
        job = sched.add_job(scheduled_job, next_run_time=next_run_time)
        print "new job scheduled at time: %s" % job.next_run_time
    
    now = datetime.now(TZ)
    time_diff = job.next_run_time + timedelta(hours=next_check_hours) 
    sleep_seconds = next_check_hours * 60 * 60
    print("next check time: %s" % time_diff)
    sleep(sleep_seconds)
