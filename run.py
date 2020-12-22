from keep_alive import keep_alive
import os
import csv
curr_dir=os.getcwd()
import apscheduler
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()
sched.start()

# Schedule job_function to be called every two hours
@sched.interval_schedule(days=7)
def job_function():
    os.chdir(curr_dir+"/youtube_last uploads/")
    file = open("database.csv", 'w')
    file.write("")
    with open('database.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "description"])
    os.chdir(curr_dir)

@sched.interval_schedule(hours=23)    
def youtube_upload():    
    os.system("python3 main.py")

keep_alive()   
