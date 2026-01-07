


''' NOTES

	TODO

		tutorial 4
		figure out how to close popup ads
			https://stackoverflow.com/questions/42008856/how-to-close-popovers-and-in-line-ads-with-selenium-webdriver

	SOURCES

		Python Selenium Tutorial Series:
			Tutorial #1 - Web Scraping, Bots & Testing					https://www.youtube.com/watch?v=Xjv1sY630Uc
			Tutorial #2 - Locating Elements From HTML					https://www.youtube.com/watch?v=b5jt2bhSeXs
			Tutorial #3 - Page Navigating and Clicking Elements			https://www.youtube.com/watch?v=U6gbGk5WPws
			Tutorial #4 - ActionChains & Automating Cookie Clicker!		https://www.youtube.com/watch?v=OISEEL5eBqg
			Tutorial #5 - UnitTest Framework (Part 1)					https://www.youtube.com/watch?v=9_5Wqgni_Xw

		Chrome WebDriver Download
			install chrome driver to the right path on linux
				sudo mv chromedriver /usr/bin/chromedriver
				sudo chown root:root /usr/bin/chromedriver
				sudo chmod +x /usr/bin/chromedriver
			https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
		https://sites.google.com/a/chromium.org/chromedriver/downloads

		Selenium Documentation
		https://selenium-python.readthedocs.io/
	
	'''



# TUTORIAL #1
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# this is differet than the tutorial because of a version upgrade
# https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
PATH = '/usr/bin/chromedriver'
service = Service(PATH)
driver = webdriver.Chrome(service=service)

URL = 'https://www.techwithtim.net/'
driver.get(URL) # open webpage
print(driver.title, '\n') # get title of webpage (aka text in the tab)

# # driver.close() # close the current tab (and entire browser if only 1 tab is open)
# driver.quit() # close entire browser


'''

# TUTORIAL #2
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# use a search bar
search = driver.find_element_by_name("s") # search by html component. in this case the "name", and the value "s". html line: <input type="search" class="search-field" placeholder="Search ..." value name="s"> == $0
search.clear() # clear search bar of any possible previous text
search.send_keys("test") # search: "test"
search.send_keys(Keys.RETURN) # hit enter

# time.sleep(5) # pause cause the example website is slow
# print(driver.page_source) # returns html of current webpage (currently the search results)

# wait for webpage to load before querying it
# https://selenium-python.readthedocs.io/waits.html
try:
	main = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "main")))
	# print(main.text)

	# print the results
	articles = main.find_elements_by_tag_name("article")
	for i, article in enumerate(articles):
		header = article.find_element_by_class_name("entry-summary")
		print('search result %d:\n' % i, header.text, '\n')
except:
	driver.quit()

# driver.quit() # close entire browser

'''



# TUTORIAL 3
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# click a link
link = driver.find_element_by_link_text("Python Programming")
link.click()

import sys
sys.exit()

# click some clickable text
# wait for webpage to load before querying it
# https://selenium-python.readthedocs.io/waits.html
try:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials")))
	element.click()
except:
	driver.quit()



# click a button
try:
	button = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(
			(By.ID, "sow-button-19310003")))
	button.click()
except:
	driver.quit()

# go back
driver.back()
driver.back()
driver.back()

# go forward
driver.forward()
driver.forward()
driver.forward()






# Tutorial #4
# https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
from selenium.webdriver.common.action_chains import ActionChains

# action chains are used to create a pre defined list of actions to execute
# that you can then command to execute at a specific point by typing actions.perform()
# in this example, we automate playing the Cookie Clicker game, where you get points 
# for clicking the cookie and can buy things with those points

URL = 'https://orteil.dashnet.org/cookieclicker/'
driver.get(URL)

driver.implicitly_wait(5) # pause program 5 seconds

cookie = driver.find_element_by_id("bigCookie")
cookie_count = driver.find_element_by_id("cookies")
items = [driver.find_element_by_id("productPrice" + str(i)) for i in [1, 0]]

actions = ActionChains(driver)
actions.click(cookie) # click where ever the mouse currently is if no argument, click the argument if given

for i in range(500):
	actions.perform() # perform the action sequence (in this case clicking the cookie)
	count = int(cookie_count.text.split(" ")[0]) # figure out how many cookies i have

	# buy items if i can afford to
	for item in items:
		value = int(item.text)
		if value <= count:
			upgrade_actions = ActionChains(driver)
			upgrade_actions.move_to_element(item)
			upgrade_actions.click()
			upgrade_actions.perform()




# Tutorial #5

