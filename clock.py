from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=13, minute=11)
def scheduled_job():
    cmd = "scrapy crawl visitcount"
    print('Running: %s' % cmd)
    subprocess.Popen(cmd, shell=True)

sched.start()
