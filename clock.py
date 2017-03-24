from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=12, minute=59)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
