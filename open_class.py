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
record_join_now_path = "//div[@class='']"
def open_class(link, runtime, class_name, record_class=False, debug_port = 6969, exec_path = "D:\Github\chromedriver_win32\chromedriver.exe", exit_browser = False):
    debug_address = "127.0.0.1:" + str(debug_port)
    cmd = "chrome --remote-debugging-port=" + str(debug_port)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debug_address)
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
    driver.minimize_window()
    driver.get(link)
    sleep(7)
    mic_off = True
    cam_off = True
    src = driver.page_source
    sleep(2)
    #Mic and cam off check
    while True:
        if "Turn off microphone" in src:
            mic_off = False
            driver.refresh()
        elif "Turn off camera" in src:
            cam_off = False
            driver.refresh()
        if mic_off and cam_off:
            break
    
    #join_class
    try:
        j = driver.find_element_by_xpath(join_now_path)
        j.click()
        send_alert(joined_class=True, class_name=class_name)
    except:
        print("Error\nCouldnt find join button")
        send_alert(joined_class=False, class_name=class_name)
    driver.quit()

    sleep(runtime) #Sleep for the duration of the class
    
    #Connect again to exit class
    driver = webdriver.Chrome(options=chrome_options, executable_path= exec_path)
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
            process.terminate()
        except:
            try:
                action = ActionChains(driver)
                action.key_down(Keys.ALT).key_down(Keys.F4).key_up(Keys.F4).key_up(Keys.ALT).perform()
            except:
                print("Error\nCouldnt exit the browser")
                send_alert(custom_msg="Error\nCouldnt exit the browser")