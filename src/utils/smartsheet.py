import os
import time
from getpass import getpass

from selenium.webdriver.firefox.webdriver import WebDriver
from utils.lcs import longest_common_substring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


from CONFIG import password, username, dashboard,threshold




def get_links(work_log: dict, driver:WebDriver):
    user:str = username
    pw:str = password
    driver.get(dashboard)    
    #Username
    if(not user):
        user = (input("Username: "))
    elem = driver.find_element_by_id("i0116") #username field
    elem.send_keys(user)
    elem = driver.find_element_by_id("idSIButton9") #submit button
    elem.click()

    #Password
    if(not pw):
        pw = getpass()
    time.sleep(2)  #This is an awful way to fix this -- should be looking for a better way to wait for a value try to get wait().until() to work
    elem = driver.find_element_by_id("i0118") #password field
    elem.send_keys(pw)
    elem = driver.find_element_by_id("idSIButton9") #submit button
    elem.click()

    #MFA
    veri_code = input("Verification code: ")
    elem = driver.find_element_by_id("idTxtBx_SAOTCC_OTC") #verification field
    elem.send_keys(veri_code)
    elem = driver.find_element_by_id("idSubmit_SAOTCC_Continue") #submit button
    elem.click()

    #Stay Signed in? --> NO
    time.sleep(2)  #This is an awful way to fix this -- should be looking for a better way to wait for a value try to get wait().until() to work
    elem = driver.find_element_by_id("idBtn_Back")
    elem.click()

    #Grab Project Table & Open (Wait for pageload)
    time.sleep(3.5)  #This is an awful way to fix this -- should be looking for a better way to wait for a value try to get wait().until() to work
    iframe = driver.find_element_by_xpath("//iframe[1]").get_attribute('src') 
    driver.get(iframe)
    time.sleep(3.5)  #This is an awful way to fix this -- should be looking for a better way to wait for a value try to get wait().until() to work

    #Loop Through Rows 
    projects = []
    count = 0 #Skip Base99 Entry 
    #grab each element from table
    for project in driver.find_elements_by_xpath("//div[@aria-label='row']")[1:]: #I don't know if this is the right fix, but it works for now so...
        title = project.find_element_by_xpath(".//div[@aria-colindex='2']/div/div").get_attribute('title')       #the name column 
        link = project.find_element_by_xpath(".//div[@aria-colindex='7']/div/div/div/a").get_attribute('href')       #the link column
        count += 1
        
        for key in work_log:
            x = title.replace(" ", "").upper()
            y = key.replace(" ", "").upper()
            length, i, j = longest_common_substring(x, y)
            if length > threshold: #and title not in projects:  #most companies are {threshold} letter abbreviations && no duplicates
                work_log[key]['Link'] = link

    #Testing
    if __name__ == '__main__':
        for i in projects:
            print(i)


    return work_log,driver.command_executor._url, driver.session_id

