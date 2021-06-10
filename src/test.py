from selenium import webdriver
from utils.calendar import get_work_log
from utils.smartsheet import get_links
from utils.log_time import log_smartsheet, _log_base99_

driver = webdriver.Firefox()

title = 'test'
description = 'desc'
start = ''
end = 'end'
link = 'link'
work_log = {}
#work_log[title] = {"Title": title, "Description": description, "Start": start,"End": end, "Link": ""}
#work_log[title]['Link'] = "http://test.com"

work_log['TEST'] = {'Title': 'Team Too Daily Stand Up [1]', 'Description': '', 'Start': '08:30', 'End': '08:45', 'Link': ''}

_log_base99_(work_log['TEST'], driver)