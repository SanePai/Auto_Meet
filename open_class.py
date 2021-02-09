import keyboard as kb
from time import sleep
import pyautogui as pg
from pyautogui import ImageNotFoundException

def open_class(link, runtime, end_time_correction = 0):
    if end_time_correction>runtime:
        print(f'Sleeping for {runtime}')
        sleep(runtime)
        return 0 
    if pg.locateOnScreen("chrome_close.png"):
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
    sleep(5)
    try:
        pg.click('join_now_button.png')
    except TypeError:
        sleep(5)
        pg.click('join_now_button.png')
    except:
        sleep(2)
        pg.click('join_now_button.png')
    # record(f"Test_Lab_Recording {runtime}.avi")
    sleep(runtime - end_time_correction)
    try:
        pg.click("end_class.png")
        sleep(1)
        kb.send('ctrl+w')
    except TypeError:
        kb.send('win+1')
        sleep(2)
        count = 0
        while True:
            if count == 6:
                print("Couldnt find the end button")
                break
            try: 
                pg.click('end_class.png')
                sleep(1)
                kb.send('ctrl+w')
            except TypeError:
                kb.send('ctrl+tab')
                count += 1
    sleep(end_time_correction)