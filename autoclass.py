from gapi import meetlinks
from time import sleep
import datetime
import os
from open_class import open_class
from send_alert import send_alert
import json

settings = json.load(open('settings.json'))
sleep_update = settings['defaults']['sleepUpdateTime']
notifs = settings['notifs']


def print_details(event):
    class_name = ""
    for i in range(2,len(event)-1):
        class_name += event[i]
        class_name += " "
    start = datetime.datetime.fromisoformat(event[0])
    end = datetime.datetime.fromisoformat(event[1])
    print(f"Class: {class_name}\n{start} to {end}")
    return class_name
        

def auto_class():
    last_class = False
    while True:
        currentTime = datetime.datetime.today()
        meetlinks()
        with open('meet.txt','r') as fh:
            st = fh.read().splitlines()
            fh.close()
        # print(datetime.datetime.fromisoformat(st[0].split()[0]))
        first_start = (st[0].split()[0])
        last_end = st[-1].split()[1]
        first_start = datetime.datetime.fromisoformat(first_start)
        last_end = datetime.datetime.fromisoformat(last_end)
        currentiso = currentTime.isoformat()

        end_times = [datetime.datetime.fromisoformat(st_.split()[1]) for st_ in st]
        index = -1
        noClassLeft = False
        if currentTime < first_start:
            sleep_time = (first_start - currentTime).total_seconds()
            print(f"First class in {sleep_time} seconds")
            m = sleep_time
            while m:
                if m<sleep_update:
                    sleep(m)
                    break
                sleep(sleep_update)
                m = (first_start - datetime.datetime.now()).total_seconds()
                print(f'First class in {first_start - datetime.datetime.now()}')
            continue
        if currentTime > last_end:
            noClassLeft = True
            break
        for end in end_times:
            if currentTime <= end:
                index = end_times.index(end)
                break
        if index<0:
            noClassLeft = True
            print("No class left")
            break
        elif index>=0:
            start_time = st[index].split()[0]
            end_time = st[index].split()[1]
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            if currentTime < start_time:
                sleep_time = (start_time - currentTime)
                while sleep_time.total_seconds():
                    print(f'Class not starting for {sleep_time}')
                    if sleep_time.total_seconds() <= sleep_update:
                        sleep(sleep_time.total_seconds())
                        break
                    sleep(sleep_update)
                    sleep_time = (start_time - datetime.datetime.now())
            elif currentTime >= start_time:
                if index == len(st)-1:
                    last_class = True
                link = st[index].split()[-1]
                runtime = (end_time - currentTime).total_seconds()
                if ".com" in link:
                    class_name = print_details(st[index].split())
                    open_class(link, runtime,class_name, exit_browser=last_class)
                else:
                    print("No meet link available for this event")
                    sleep(runtime)
            else:
                print("Unknown Error")
                if notifs:
                    send_alert(custom_msg="Some unknown error has occured")
            if noClassLeft: break
    if noClassLeft:
        return noClassLeft

if __name__ == "__main__":
    auto_class()