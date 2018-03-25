from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import os
import unittest

loginurl = "https://test.salesforce.com"
userid = 
pwd = 

sessionfile = "ch" + "_" + userid
remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
sessionfile = sessionfile.translate(remove_punctuation_map)
reuseSession = True #False
# http://tarunlalwani.com/post/reusing-existing-browser-session-selenium/

SESSION_ID = "session_id"
EXECUTOR_URL = "executor_url"
USERNAME_TBX_NAME = "username"
PASSWORD_TBX_NAME = "pw"

def sendKeys(elem, key, delay = 3):
    time.sleep(delay)
    elem.send_keys(key)

def TestPermissions():
    driver = Login(reuseSession)
   
    leadsLink = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@title,'Leads')]"))
    )
    sendKeys(leadsLink, Keys.RETURN, 7)

    leadLink = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@title,'Friday Test')]"))
    )
    sendKeys(leadLink, Keys.RETURN)
    
    time.sleep(3)
    cdTaskLink = driver.find_element_by_xpath("//a[contains(@title,'CD Task')]")
    assert "CD Task" in cdTaskLink.text
    vipTaskLink = driver.find_element_by_xpath("//a[contains(@title,'VIP Task')]")
    assert "VIP Task" in vipTaskLink.text

    sendKeys(cdTaskLink, Keys.RETURN)

    addButton = WebDriverWait(driver, 5).until(
    # EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'Add')]"))
        EC.element_to_be_clickable((By.XPATH, "//span[text() = 'Add']"))
    )
    # addButton = driver.find_element_by_xpath()
    addButton.click()
    # sendKeys(addButton, Keys.RETURN)

    time.sleep(2)
    tomOrderfld = driver.find_element_by_xpath("//span[text() = 'TOM Order Number']")
    assert 'TOM Order Number' in tomOrderfld.text

def create_driver_session(session_id, executor_url):
    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    return new_driver

def Login(reuseSession):
    if not(reuseSession):
        driver = webdriver.Chrome()
        executor_url = driver.command_executor._url
        session_id = driver.session_id
        driver.get(loginurl)
        assert "Salesforce" in driver.title

        session = {SESSION_ID : session_id, EXECUTOR_URL : executor_url }
        with open(sessionfile, 'wb') as handle:
            pickle.dump(session, handle, protocol=pickle.HIGHEST_PROTOCOL)

        login_tbx = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, USERNAME_TBX_NAME))
        )
        
        login_tbx.clear()
        login_tbx.send_keys(userid)

        pwd_tbx = driver.find_element_by_name(PASSWORD_TBX_NAME)
        pwd_tbx.clear()
        pwd_tbx.send_keys(pwd)

        pwd_tbx.send_keys(Keys.RETURN)

    else:
        with open(sessionfile, 'rb') as handle:
            b = pickle.load(handle)

        session_id = b.get(SESSION_ID)
        executor_url = b.get(EXECUTOR_URL)
        driver = create_driver_session(session_id, executor_url)
        driver.get(loginurl)

        login_tbx = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, USERNAME_TBX_NAME))
        )
        login_tbx.clear()

        login_tbx.send_keys(userid)

        pwd_tbx = driver.find_element_by_name(PASSWORD_TBX_NAME)
        pwd_tbx.clear()
        pwd_tbx.send_keys(pwd)

        pwd_tbx.send_keys(Keys.RETURN)

    return driver

TestPermissions()
