import time
from datetime import date

from selenium import webdriver
from selenium.common import exceptions as sel_exceptions
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime, timedelta, timezone

# .// is for context specific (i.e. find_elements...(//foo) find_element...(.//bar) would grab //foo/bar:)
actions:ActionChains
body:WebElement


#TODO Implement
def _log_base99_(log,driver):
    driver.get("https://app.base99.com/sso/")
    
    #make new ticket
    elem = driver.find_element_by_class_name("add-new-ticket")
    elem.click()

    #select template
    elem = Select(driver.find_element_by_id("mxui_widget_ReferenceSelector_0_input"))
    elem.select_by_index(0)

    #change time to 5:00 AM current day
    elem = driver.find_element_by_xpath("//div[@class='react-datepicker__input-container']//input[@type='text']")
    curDay = datetime.today().strftime("%m/%d/%Y");
    elem.send_keys(curDay + " 5:00 AM")
    elem.send_keys(Keys.RETURN)

    #enter description
    elem = driver.find_element_by_xpath("//div[@class='cke_wysiwyg_div cke_reset cke_enable_context_menu cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")
    elem.send_keys("Time Entry by TIMEBOT")

    #create and view
    elem = driver.find_element_by_xpath("//button[text()='Create and view']")
    elem.click()

    time.sleep(4) #STUPID STUPID STUPID

    #add notes/labor
    elem = driver.find_element_by_xpath("//button[text()='Notes/Labor']")
    elem.click()

    #description
    elem = driver.find_element_by_xpath("//div[@id='cke_155_contents']//div[@class='cke_wysiwyg_div cke_reset cke_enable_context_menu cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']")
    elem.send_keys(log['Title'])

    #convert time to 12HR
    start = datetime.strptime(log['Start'], "%H:%M")
    start.strftime(("%I:%M %p"))

    end = datetime.strptime(log['End'],("%I:%M %p"))
    end.strftime(("%I:%M %p")) 

    #add labor
    elem = driver.find_element_by_xpath("//a[@class='mx-link mx-name-actionButton2 spacing-outer-left']") 
    elem.click()
    time.sleep(4) #STUPID

    elem = Select(driver.find_element_by_xpath("//select[@id='mxui_widget_ReferenceSelector_10_input']"))
    elem.select_by_index(0)

    elem = driver.find_element_by_xpath("//div[@class='mx-name-dateTimePicker1 form-group no-columns']//div[@class='react-datepicker-wrapper']//div[@class='react-datepicker__input-container']//input[@type='text']")
    elem.send_keys(curDay + " " + start)

    elem = driver.find_element_by_xpath("//div[@class='mx-name-dateTimePicker2 form-group no-columns']//div[@class='react-datepicker-wrapper']//div[@class='react-datepicker__input-container']//input[@type='text']")
    elem.send_keys(curDay + " " + end)

    #click confirm
    elem = driver.find_element_by_xpath("//button[text()='Confirm']")
    elem.click()
    time.sleep(4) #STUPID

    #TODO FINISH ME ---> click complete and finish it off
    

    

    return

def _base_99_in_progress(log,driver):
    print("The following calendar entry has no matches in your smartsheet dashboard and will need to be entered on BASE99 manually:\n" + str(log))


#FIXME won't work for values that aren't a multiple of 15 --> Check in the calendar one and fix it there
#Finds the form field and enters required information
def __enter_value__(field,log_item):
    x_body_offset = body.location["x"]
    y_body_offset = body.location["y"]
    e_loc = field.location
    x = e_loc['x']
    y = e_loc['y']
    actions.move_to_element_with_offset(body, -x_body_offset, -y_body_offset).click() #might not need .click()
    actions.move_by_offset( x, y ).click()
    actions.send_keys(log_item + Keys.ENTER).perform()

#TODO loop through dict, open up time entries, fill out data
def log_smartsheet(work_log:dict,remote_executor:str,session_id:str,driver:WebDriver):

    for log in work_log:

        print(work_log[log]["Title"] + ":")

        #no link for this one: 
        #TODO ask to log in base99
        try:  
            driver.get(work_log[log]["Link"])
            global body #this is so stupid, why can't i just use one line for these
            body = driver.find_element_by_tag_name('body')
            global actions #this is so stupid, why can't i just use one line for these
            actions = ActionChains(driver)
        except sel_exceptions.InvalidArgumentException:
                work_log[log]["Link"] = "base99"
                _base_99_in_progress(work_log[log],driver)
                continue

            #check for radio button, #TODO maybe there's a way to not require user input?
        try: 
            field:WebElement = driver.find_element_by_xpath("//form/div/fieldset/legend")
            
            opts:list[WebElement] = field.find_elements_by_xpath("//form/div/fieldset/div/div")
            input_string = "Which project did you work on?\n"
            count = 0
            for option in opts:
                input_string += option.text + "    [" + str(count) + "]" + "\n"
                count += 1

            selected_option = int(input(input_string))
            opts[selected_option].find_element_by_xpath(".//label/input").click()
        except sel_exceptions.NoSuchElementException:  #if not found
            pass
        
        if not work_log[log]["Description"]:
            work_log[log]["Description"] = input("Enter a description for what you did:\n")
        time.sleep(2)
        field  = driver.find_element_by_xpath("//input[@id='text_box_Comments']") #Comments
        field.send_keys(work_log[log]["Description"])

        time.sleep(2)
        field  = driver.find_element_by_xpath("//input[@id='select_input_Labor Start (Military)']") #Labor Start
        __enter_value__(field, work_log[log]["Start"])

        time.sleep(2)
        field  = driver.find_element_by_xpath("//input[@id='select_input_Labor End (Military)']") #Labor End
        __enter_value__(field, work_log[log]["End"])


        field  = driver.find_element_by_xpath("//input[@id='date_Actual Start Date']") #Actual Start Date
        field.click()
        field.send_keys(date.today().strftime("%d/%m/%Y"))

        if input("Does this look correct? (Y/n): ") == 'Y':
            field  = driver.find_element_by_xpath("//button[@type='submit']") #Submit 
            field.click()
            time.sleep(12)
            print("Submitted: " + str(work_log[log]))
        else:
            input("Please fix incorrect values and click submit\n[Press Enter to Continue]")
        

    return

