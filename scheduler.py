from crontab import CronTab

#cron = CronTab(user='spashankova')  
cron = CronTab(tabfile='filename.tab')
job = cron.new(command='C:/Users/spashankova/BicingPy/tracking+availability.py')  
job.minute.every(5)

cron.write()  