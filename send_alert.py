import os
from time import sleep
from notify_run import Notify
def send_alert(joined_class=None, exit_class=None, link=None, custom_msg = None):
    notify = Notify()
    if joined_class:
        msg = "Joined class succesfully"
        notify.send(msg)
    if exit_class:
        msg = "Exited class succesfully"
        notify.send(msg)
    if joined_class is False:
        msg = "Failed to join class"
        notify.send(msg, link)
    if exit_class is False:
        msg = "Failed to exit class"
        notify.send(msg)
    if custom_msg:
        notify.send(custom_msg)