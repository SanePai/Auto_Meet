from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import subprocess
import selenium.common.exceptions
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from send_alert import send_alert

join_now_path = "//span[@class='NPEfkd RveJvd snByac']"
end_class_path = "//span[@class='DPvwYc JnDFsc grFr5 FbBiwc']"
record_join_now_path = "//span[@class='RveJvd snByac']"
def open_class(link, runtime, class_name, record_class=False, debug_port = 6942, exec_path = "D:\Github\chromedriver_win32\chromedriver.exe", user_data_dir = "D:\Github\Auto_Meet\sel_profile", exit_browser = False):
    if "https://" not in link:
        link = "https://" + link
    
    debug_address = "127.0.0.1:" + str(debug_port)
    cmd = "chrome --remote-debugging-port=" + str(debug_port) + " --user-data-dir=" + user_data_dir
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debug_address)
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
    sleep(10)
    mic_off = True
    cam_off = True
    src = driver.page_source
    sleep(2)
    #Mic and cam off check
    while True:
        if "Turn on microphone" in src and "Turn on camera" in src:
            break
        else:
            driver.refresh()
            sleep(3)
            src = driver.page_source

    #join_class
    try:
        j = driver.find_element_by_xpath(join_now_path)
        j.click()
        send_alert(joined_class=True, class_name=class_name)
    except:
        print("Error\nCouldnt find join button")
        send_alert(joined_class=False, class_name=class_name)
    
    #Check for join in case of recording

    src = driver.page_source
    if "This meeting is being recorded" in src:
        try:
            r = driver.find_element_by_xpath(record_join_now_path)
            r.click()
        except:
            send_alert(custom_msg = "Joined class but couldnt get past record screen")

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