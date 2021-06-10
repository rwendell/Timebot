from selenium import webdriver
from utils.calendar import get_work_log
from utils.smartsheet import get_links
from utils.log_time import log_smartsheet


# TODO		add template maker with JSON in description for easier adding (New Data Entry type found would you like to save this as a template for easier use in the future?)
# TODO		Caching for table maybe? only check for updates onces every month?
# FIXME		Labor Start Gets Double-Typed  
# TODO		Group all base99 together and then add them using a single base99 ticket		

work_log = {}
work_log = get_work_log()
driver = webdriver.Firefox()
work_log,remote_executor,session_id = get_links(work_log,driver)
log_smartsheet(work_log, remote_executor,session_id,driver)
driver.close()



