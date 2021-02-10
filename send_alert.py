import os
from time import sleep
from notify_run import Notify
def send_alert(joined_class=None, exit_class=None, link=None, custom_msg = None, class_name = None):
    notify = Notify()
    if joined_class:
        msg = f"Joined class succesfully\nClass: {class_name}"
        notify.send(msg)
    if exit_class:
        msg = f"Exited class succesfully\nClass: {class_name}"
        notify.send(msg)
    if joined_class is False:
        msg = f"Failed to join class\nClass: {class_name}. Click to join"
        notify.send(msg, link)
    if exit_class is False:
        msg = f"Failed to exit class\nClass: {class_name}"
        notify.send(msg)
    if custom_msg:
        notify.send(custom_msg)