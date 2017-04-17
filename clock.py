from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
import sys
import random
from time import sleep
from datetime import datetime
from datetime import timedelta 
import pytz
import pymongo
import gridfs
import logging

hour_start = 2
hour_end = 5
minute_start = 0
minute_end = 59
in_between_delay_minute = 5
scrapy_time = 30 # minute
next_check_hours = 20

TZ=pytz.timezone("Asia/Taipei")

MONGODBCSV_URI=os.environ["MONGODBCSV_URI"]
client = pymongo.MongoClient(MONGODBCSV_URI)
db = client["csv"]
fs_db = gridfs.GridFS(db)

logging.basicConfig(format='%(filename)s:%(levelname)s:%(message)s', level=logging.DEBUG)

def save_csv(new_date):
    home = os.environ.get("HOME","/tmp")
    csv_file = os.path.join(home, "visitcount.csv") 

    new_filename = "%s.csv" % new_date

    with open(csv_file, 'r') as fp_local:
        with fs_db.new_file(filename=new_filename) as fp_remote:
            fp_remote.write(fp_local.read())


def scheduled_job():
    cmd = os.environ.get("SCRAPY_CMD",None)
    logging.debug('Late night crawler is running: %s' % cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    new_date = str(datetime.now(TZ).date())
    logging.debug('save visitcount.csv as %s.csv in gridfs' % new_date)
    save_csv(new_date)

def get_next_run_time(is_refresh_run):
    now = datetime.now(TZ)
    
    if( is_refresh_run ):
        next_run_time_ = now
    else:
        hour=random.randint(hour_start,hour_end)
        minute=random.randint(minute_start,minute_end)

        start_time = datetime(next_run_time.year,next_run_time.month,next_run_time.day,hour_start,minute_start,tzinfo=TZ)
        end_time = start_time.replace(hour=hour_end, minute=minute_end)
    
        logging.debug("next_run_time: %s" % next_run_time)
        logging.debug("start_time: %s" % start_time)
        logging.debug("end_time: %s" % end_time)
        if start_time <= now <= end_time:
            logging.debug("now in between")
            next_run_time_ = now + timedelta(minutes=in_between_delay_minute)
        elif now < start_time:
            logging.debug("now < start_time")
            next_run_time_ = next_run_time.replace(hour=hour,minute=minute)
        else:
            logging.debug("now > end_time")
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
        logging.debug("new job scheduled at time: %s" % job.next_run_time)
    
    time_diff = job.next_run_time + timedelta(hours=next_check_hours) 
    sleep_seconds = next_check_hours * 60 * 60
    logging.debug("next check time: %s" % time_diff)
    sleep(sleep_seconds)
