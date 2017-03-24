from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=13, minute=2)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
