'''import sys

def my_scheduled_job():
    print "Hello"
    return True

my_scheduled_job()'''

'''import sys
from crontab import CronTab
#init cron
cron   = CronTab()

#add new cron job
job  = cron.new(command='print "HELLO"')

#job settings
job.minute.every(1)'''

from django_cron import CronJobBase, Schedule
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time


class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1 # every 2 hours

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'my_app.my_cron_job'    # a unique code

	def do(self):
		print "START!"
		# current_directory = os.getcwd()
		# with open(current_directory + '/ultimatefitbackend/python_cron_test.json', 'w') as f:
		# 	f.write("Hello from CRON! The time now is: " + str(datetime.now()))
		# 	f.close()

		chrome_options = Options()
		print chrome_options
		chrome_options.add_argument("--headless")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('window-size=1920x1480')

		global driver
		driver = webdriver.Chrome(chrome_options=chrome_options)
		print driver

		# First have to log in
		driver.get("https://lokalise.co/login")
		# WebDriverWait(driver, 10).until(ExpectedConditions.presenceOfElementLocated(By.id("go-login")));
		# print "Hi testing1"

		assert "Log in | Lokalise" in driver.title

		username = driver.find_element_by_id("signinEmail")
		password = driver.find_element_by_id("signinPassword")

		username.send_keys("twohourbinhyen@gmail.com")
		password.send_keys("iahk9425")
		print "Hi testing3", driver.find_element_by_id("go-login")
		# time.sleep(5)
		# WebDriverWait(driver, 5)
		driver.find_element_by_id("go-login").click()
		print "test first 1"

		# assert "Lokalise | App localization. Translation platform, services & tools." in driver.title

		print "test first 2"

		driver.implicitly_wait(10) # This is the correct way to wait LoL
		# Then navigate to the correct link and crawl
		# driver.get("https://lokalise.co/project/459393505c7d537f70b824.54792573/?view=single&reference_lang_id=640&single_lang_id=774")
		# driver.find_element_by_css_selector("a[href='/project/459393505c7d537f70b824.54792573/?view=multi']").click()
		# driver.find_element_by_css_selector("[@href='/project/459393505c7d537f70b824.54792573/?view=multi']").click()


		# driver.get("https://www.google.com")
		# print "done google"
		# driver.implicitly_wait(10)

		#####################################################################

		project_stat_collector = driver.find_elements_by_css_selector(".project-stat-title a")
		for item in project_stat_collector:
			if (item.text == "translate by keys"):
				print item
				item.click()
				break
		# print driver.current_url
		# assert "translate by keys" in driver.title

		print "test"

		driver.implicitly_wait(10)

		# keys_container = driver.find_element_by_id("endless")
		keys_container = driver.find_element_by_css_selector("#endless div.page.current")
		print "keys_container", keys_container
		keys_collection = keys_container.find_elements_by_css_selector(".row-key")
		print "keys_collections", keys_collection


		final_translation_str = "{\n"

		for index, key_word in enumerate(keys_collection):
			translated_text_container = key_word.find_elements_by_css_selector("div.col-md-9.break-word table tbody tr.row-trans.translation")[1]

			translation_label = key_word.get_attribute("data-name")
			translation_en = key_word.get_attribute("data-base-translation")
			translation_vn = translated_text_container.find_element_by_css_selector("td.cell-trans div.clearfix div.modified-info-wrapper").get_attribute("data-value")

			if (type(translation_label) != "" and str(type(translation_label)) == "<type 'unicode'>") and (type(translation_en) != "" and str(type(translation_en)) == "<type 'unicode'>") and (type(translation_vn) != "" and str(type(translation_vn)) == "<type 'unicode'>"):
				if index == len(keys_collection) - 1:
					final_translation_str += '\t"' + str(translation_label) + '": {"vn": "' + str(translation_vn.encode('utf8')) + '","en": "' + str(translation_en) + '"}\n'
				else:
					final_translation_str += '\t"' + str(translation_label) + '": {"vn": "' + str(translation_vn.encode('utf8')) + '","en": "' + str(translation_en) + '"},\n'

		final_translation_str += "}"
		driver.close()

		current_directory = os.getcwd()
		with open(current_directory + '/ultimatefitbackend/python_cron_test.json', 'w') as f:
			f.write(final_translation_str)
			f.close()

		print "DONE!"
