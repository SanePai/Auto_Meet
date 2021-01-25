import keyboard as kb
from time import sleep
import pyautogui as pg
from pyautogui import ImageNotFoundException

def open_class(link, runtime):
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
        pg.locateOnScreen('join_now_button.png')
    except ImageNotFoundException:
        sleep(5)
    pg.click('join_now_button.png')
    # sleep(1)
    # record(f"Test_Lab_Recording {runtime}.avi")
    sleep(runtime)
    # m = runtime
    # while m>0:
    #     print(f'{m} left')
    #     sleep(10)
    #     m = m - 10
    try:
        pg.click("end_class.png")
        sleep(1)
        kb.send('ctrl+w')
    except ImageNotFoundException:
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
            except ImageNotFoundException:
                kb.send('ctrl+tab')
                count += 1

if __name__ == "__main__":
    open_class()