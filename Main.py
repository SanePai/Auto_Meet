from autoclass import auto_class
import datetime
from time import sleep
from send_alert import send_alert
import json

def main():
    settings = json.load(open('settings.json'))
    weekdays = settings['weekdays']
    sleep_update = settings['defaults']['sleepUpdateTime']
    notifs = settings['notifs']
    weekend_gap = 8 - weekdays
    end_of_week = weekdays - 1
    now = datetime.datetime.now()
    noClassLeft = auto_class()
    if noClassLeft:
        now = datetime.datetime.now()
        if now.weekday() == end_of_week: #Skip weekends
            # gap = weekend_gap
            gap = datetime.timedelta(weekend_gap)
        else:
            gap = datetime.timedelta(1) 
        tom = datetime.datetime(now.year, now.month, now.day, 8, 00, 00) + gap
        print("Done for today")
        if notifs:
            send_alert(custom_msg="Done for today\nSleeping till tomorrow")
        with open('meet.txt', 'w') as fh: #Delete all entries in the meet links file
            pass
        print(f'Sleeping for {(tom - now)}')
        m = (tom-now).total_seconds()
        while m>=0:
            if m <= sleep_update:
                sleep(m)
                break
            sleep(sleep_update)
            m = (tom - datetime.datetime.now()).total_seconds()
    main()

if __name__ == "__main__":
    main()