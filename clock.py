from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import random

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=random.randint(2,6), minute=random.randint(0,60))
def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Late night crawler is running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)

sched.start()
