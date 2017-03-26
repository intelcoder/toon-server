from django_cron import CronJobBase, Schedule



class TestCron(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'webtoon.test'

    def do(self):
        print("cron is working")
