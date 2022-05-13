from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()



@sched.scheduled_job_am('cron', day_of_week='mon-sun', hour=6)
def scheduled_job_am():
    print('6 AM weather check')

@sched.scheduled_job_noon("cron", day_of_week="mon-sun", hour=12)
def scheduled_job_noon():
    print("12 PM weather check")

@sched.scheduled_job_afternoon("cron", day_of_week="mon-sun", hour=15)
def scheduled_job_afternoon():
    print("3 PM weather check")

sched.start()
