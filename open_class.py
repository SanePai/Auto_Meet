from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import subprocess
import selenium.common.exceptions
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from send_alert import send_alert
import json

settings = json.load(open('settings.json'))
join_now_path = settings['elementPaths']['join_now_path']
end_class_path = settings['elementPaths']['end_class_path']
record_join_now_path = settings['elementPaths']['record_join_now_path']
exec_path = settings['defaults']['seleniumExecutable']
user_data_dir = settings['defaults']['seleniumProfile']
debug_port = settings['defaults']['defaultPort']
minimize_after_join = settings['defaults']['minimizeWindowAfterJoin']
mute = settings['defaults']['muteAudio']

def open_class(link, runtime, class_name, record_class=False, 
                debug_port = debug_port, exec_path = exec_path,
                user_data_dir = user_data_dir, exit_browser = True):    
    if "https://" not in link:
        link = "https://" + link
    
    debug_address = "127.0.0.1:" + str(debug_port)
    cmd = "chrome --remote-debugging-port=" + str(debug_port) + " --user-data-dir=" + user_data_dir
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debug_address)
    if mute:
        chrome_options.add_argument("--mute-audio")
    try:
        print("Trying to connect to driver")
        driver = webdriver.Chrome(options=chrome_options, executable_path=exec_path)
        print("Connected")
    except selenium.common.exceptions.WebDriverException as e:
        print("Couldnt connect\nTrying to open")
        if 'cannot connect to chrome at' in str(e):
            process = subprocess.Popen(cmd)
            print("Trying to connect")
            driver = webdriver.Chrome(options=chrome_options, executable_path=exec_path)
            print("Connected")
        else:
            print("unknown error")
    driver.get(link)
    driver.maximize_window()
    sleep(10)
    mic_off = True
    cam_off = True
    src = driver.page_source
    sleep(2)
    #Mic and cam off check
    count = 0
    while True:
        if count == 10:
            send_alert(custom_msg= "Couldnt swtich off camera or mic")
            break
        if "Turn on microphone" in src and "Turn on camera" in src:
            break
        else:
            count += 1
            driver.refresh()
            sleep(3)
            src = driver.page_source
    ask_to_join = False
    if "Ask to join" in src:
        ask_to_join = True

    #join_class
    try:
        j = driver.find_element_by_xpath(join_now_path)
        j.click()
        if not ask_to_join:
            send_alert(joined_class=True, class_name=class_name)
        while ask_to_join:
            sleep(30) #wait 30 seconds for someone to accept (10*30 seconds = 5 minutes)
            src = driver.page_source
            if "Ask to join" not in src:
                ask_to_join = False
                send_alert(joined_class=True, class_name=class_name)
            if count == 10 or "You can't join this call" in src:
                send_alert(joined_class=False,class_name=class_name)
                send_alert(custom_msg="Join request was not accepted")
    except:
        print("Error\nCouldnt find join button")
        send_alert(joined_class=False, class_name=class_name)
    
    #Check for additional join confirmation in case of recording
    src = driver.page_source
    if "This meeting is being recorded" in src:
        try:
            r = driver.find_element_by_xpath(record_join_now_path)
            r.click()
        except:
            send_alert(custom_msg = "Joined class but couldnt get past record screen")
    if minimize_after_join:
        driver.minimize_window()
    driver.quit()

    sleep(runtime) #Sleep for the duration of the class
    
    #Connect again to exit class
    try:
        print("Connecting to driver")
        driver = webdriver.Chrome(options=chrome_options, executable_path= exec_path)
        print("Connected")
    except:
        print("Couldnt connect to driver")
        send_alert(exit_class=False)
    #Check if the host ended the meeting before
    src = driver.page_source
    if "The meeting has ended" in src:
        print("Meeting ended by host before end time")
        send_alert(custom_msg="Meeting ended by host before end time")
    else:
        try:
            l = driver.find_element_by_xpath(end_class_path)
            l.click()
            send_alert(exit_class=True, class_name=class_name)
        except:
            print("Error\nCouldnt find the exit button")
            send_alert(exit_class=False, class_name=class_name)
    

    if not exit_browser:
        driver.quit()
    elif exit_browser:
        try:
            driver.close()
            driver.quit()
        except:
            try:
                process.terminate()
            except:
                try:
                    action = ActionChains(driver)
                    action.key_down(Keys.ALT).key_down(Keys.F4).key_up(Keys.F4).key_up(Keys.ALT).perform()
                except:
                    print("Error\nCouldnt exit the browser")
                    send_alert(custom_msg="Error\nCouldnt exit the browser")