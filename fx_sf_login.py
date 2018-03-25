from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os

loginurl = "https://test.salesforce.com"
userid = 
pwd = 
sessionfile = "ch" + "_" + userid

reuseSession = False
# http://tarunlalwani.com/post/reusing-existing-browser-session-selenium/
# https://success.salesforce.com/answers?id=9063A000000iQjhQAE

SESSION_ID = "session_id"
EXECUTOR_URL = "executor_url"
USERNAME_TBX_NAME = "username"
PASSWORD_TBX_NAME = "pw"

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

if not(reuseSession):
    driver = webdriver.Chrome()
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    driver.get(loginurl)
    assert "Salesforce" in driver.title

    session = {SESSION_ID : session_id, EXECUTOR_URL : executor_url }
    with open(sessionfile, 'wb') as handle:
        pickle.dump(session, handle, protocol=pickle.HIGHEST_PROTOCOL)

    login_tbx = driver.find_element_by_name(USERNAME_TBX_NAME)
    login_tbx.clear()

    login_tbx.send_keys(userid)

    pwd_tbx = driver.find_element_by_name(PASSWORD_TBX_NAME)
    pwd_tbx.clear()
    pwd_tbx.send_keys(pwd)

    pwd_tbx.send_keys(Keys.RETURN)

    src = driver.page_source
    time.sleep(60) 

else:
    with open(sessionfile, 'rb') as handle:
        b = pickle.load(handle)

    session_id = b.get(SESSION_ID)
    executor_url = b.get(EXECUTOR_URL)
    driver2 = create_driver_session(session_id, executor_url)
    # print(driver2.current_url)
    driver2.get(loginurl)

    login_tbx = driver2.find_element_by_name(USERNAME_TBX_NAME)
    login_tbx.clear()

    login_tbx.send_keys(userid)

    pwd_tbx = driver2.find_element_by_name(PASSWORD_TBX_NAME)
    pwd_tbx.clear()
    pwd_tbx.send_keys(pwd)

    pwd_tbx.send_keys(Keys.RETURN)

    src = driver2.page_source
    time.sleep(60)
    