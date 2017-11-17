'''import sys

def my_scheduled_job():
    print "Hello"
    return True

my_scheduled_job()'''

'''import sys
from crontab import CronTab
#init cron
cron   = CronTab()

#add new cron job
job  = cron.new(command='print "HELLO"')

#job settings
job.minute.every(1)'''

from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        print "Hello from CRON!"    # do your thing here