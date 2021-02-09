import os
from time import sleep
from notify_run import Notify
def send_alert(joined_class=None, exit_class=None, link=None):
    notify = Notify()
    if joined_class:
        msg = "Joined class succesfully"
        notify.send(msg)
    if exit_class:
        msg = "Exited class succesfully"
        notify.send(msg)
    if not joined_class:
        msg = "Failed to join class"
        notify.send(msg, link)
    if not exit_class:
        msg = "Failed to exit class"
        notify.send(msg)

        msg = "Failed to join or exit class!"
        os.system(f"notify-run send \"{msg}\"", link)
send_alert(True)
sleep(5)
send_alert(False)