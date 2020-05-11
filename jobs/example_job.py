import time
import traceback

from jobs.jobs_mgr import *


def example_job():
    while not jobs_mgr.do_stop:
        print("WORKING ON EXAMPLE JOB...")

        #run every 5 minutes
        for i in range(0,600):
            if jobs_mgr.do_stop:
                return
            time.sleep(0.5)