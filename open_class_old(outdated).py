import keyboard as kb
from time import sleep
import pyautogui as pg
from pyautogui import ImageNotFoundException
from send_alert import send_alert

def open_class(link, runtime, class_name, end_time_correction = 0):
    if end_time_correction>runtime:
        print(f'Sleeping for {runtime}')
        sleep(runtime)
        return 0 
    if pg.locateOnScreen("img/chrome_close.png"):
        open_chrome = False
    else:
        open_chrome = True
    # print(open_chrome)
    if open_chrome:
        kb.send('win+1')
        sleep(7)
    kb.send('ctrl+t')
    sleep(1)
    kb.write(link)
    kb.send('enter')
    sleep(6)
    try:
        pg.click('img/join_now_button.png')
        send_alert(joined_class=True, class_name=class_name)
    except TypeError:
        try:
            sleep(6)
            pg.click('img/join_now_button.png')
            send_alert(joined_class=True, class_name=class_name)
        except:
            send_alert(joined_class=False, link = link, class_name= class_name)
    # record(f"Test_Lab_Recording {runtime}.avi")
    sleep(runtime - end_time_correction)
    try:
        pg.click("img/end_class.png")
        sleep(1)
        kb.send('ctrl+w')
        send_alert(exit_class=True, class_name= class_name)
    except TypeError:
        kb.send('win+1')
        sleep(2)
        count = 0
        while True:
            if count == 10:
                print("Couldnt find the end button")
                send_alert(exit_class=False, class_name=class_name)
                break
            try: 
                pg.click('img/end_class.png')
                sleep(1)
                kb.send('ctrl+w')
                send_alert(exit_class=True, class_name= class_name)
                break
            except TypeError:
                kb.send('ctrl+tab')
                count += 1
    sleep(end_time_correction)