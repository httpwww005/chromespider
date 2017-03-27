from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 
import pytz


def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)


def get_next_run_time(is_refresh_run):
    now = datetime.now(TZ)
    hour=random.randint(hour_start,hour_end)
    minute=random.randint(minute_start,minute_end)

    if( is_refresh_run ):
        year = now.year
        month = now.month
        day = now.day
        next_run_time_ = datetime(year,month,day,hour,minute)
    else:
        start_time = datetime(now.year,now.month,now.day,hour_start,minute_start)
        end_time = datetime(now.year,now.month,now.day,hour_end,minute_end)

        if start_time <= now <= end_time:
            next_run_time_ = next_run_time + timedelta(minutes=in_between_delay_minute)
        elif now < start_time:
            next_run_time_ = next_run_time
        else:
            next_run_time_ = next_run_time + timedelta(days=1)
            next_run_time_ = next_run_time_.replace(hour=hour,minute=minute)

    return next_run_time_


hour_start = 2
hour_end = 5
minute_start = 0
minute_end = 59
in_between_delay_minute = 5
scrapy_time = 30 # minute

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
    time_diff = job.next_run_time - now
    total_sleep = time_diff.total_seconds() + scrapy_time * 60
    print("sleep now for: %s" % str(timedelta(seconds=total_sleep)))
    sleep(total_sleep)
