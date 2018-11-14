#!/usr/bin/env python
"""
GOBii Extracor UI Datasets testing

Steps:
1. Loads Extractor UI site
2. Waits until login form is loaded
3. Log in to ExtractorUI website with a given username and password defined in properties file
4. Checks if successfully logged in
5. Clicks "By Dataset" tab
6. Loop through dropdown fields (i.e. Principal investigator, Projects, Experiment, Mapset)
7. Selects values from the dropdown lists based from the defined values in properties file
8. Selects Export file format
9. Selects datasets based from the config file
10. Clicks submit button
11. Checks if extraction was successful
12. Exit

Tests if user is able to successfully extract data from GOBii's ExtractorUI. 
User credentials and inputted values are stored in properties file 
so it can be easily modified
Created on November 2018

@author: jpramos
"""

from __future__ import print_function
import xmlrunner
import unittest
import xmlrunner
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import ConfigParser
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# default if field is not in config file
defaults = {
    'datasets.principalInvestigator': None,
    'datasets.project': None,
    'datasets.experiment': None,
    'datasets.exportFormat': None,
    'datasets.datasets': None,
    'datasets.mapset': None
}

# get values from config properties file
config = ConfigParser.RawConfigParser(defaults = defaults)
config.read('ConfigFile.properties')
extractorUILink = config.get('SiteSection','site.address') # Extractor UI address
username = config.get('UserAccountSection', 'user.username') # username
password = config.get('UserAccountSection', 'user.password') # password

# xPath variables
loginCheckBoxXpath = "//p-checkbox[@id='LOGIN_AGREE_TO_TERMS_CHECKBOX']" # checkbox in the login page
usernameXpath = "//input[@id='LOGIN_USER_NAME_INPUT']" # username field in the login page
passwordXPath = "//input[@id='LOGIN_PASSWORD_INPUT']" # password field in the login page
loginButtonXpath = "//button[@id='LOGIN_SUBMIT_BUTTON']" # login buttom
principalInvestigatorXpath = "//select[@id='NAME_ID_LIST_Contact-Pi-Filter-Optional']" # principal investigator dropdown list
projectXpath = "//select[@id='NAME_ID_LIST_Project-Filter-Optional']" # project dropdown list
experimentXpath = "//select[@id='NAME_ID_LIST_Experiment-Filter-Optional']" # experiment dropdown list
mapsetXpath = "//select[@id='NAME_ID_LIST_Mapsets']" # experiment dropdown list
submitButtonXpath = "//button[@id='SUBMIT_BUTTON_EXTRACT']" # submit button
datasetTabXpath = ".//span[contains(text(), 'By Dataset')]" # Dataset tab
sleepTime = 1

class ExtractorUITest(unittest.TestCase):

    # driver set up
    @classmethod
    def setUp(self):
       
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        # check for mode 1: Normal, 2: Headless
        if (self.mode == '2'):
            options.add_argument('--headless')
            sleepTime = 0

        self.driver = webdriver.Chrome(chrome_options=options)

    # log in
    def test_log_in(self):
        
        try:
            print("\nLogging in...\n")
            driver = self.driver

            # load extractor UI website defined in the properties file
            driver.get(extractorUILink)
            self.assertIn("GOBii Extractor", driver.title)

            # maximize window
            driver.maximize_window()

            # wait until the form is loaded
            WebDriverWait(driver, 900).until(
                EC.presence_of_element_located((By.ID, "LOGIN_AGREE_TO_TERMS_CHECKBOX"))
            )

            time.sleep(sleepTime)

            # click first checkbox element
            checkboxField = driver.find_element_by_xpath(loginCheckBoxXpath)
            checkboxField.click()

            # find first input element with name username and input username
            usernameField = driver.find_element_by_xpath(usernameXpath) 
            usernameField.send_keys(username)

            # find first input element with name password and input password
            passwordField = driver.find_element_by_xpath(passwordXPath)
            passwordField.send_keys(password)

            # click login button
            loginButton = driver.find_element_by_xpath(loginButtonXpath)
            loginButton.click()

            time.sleep(sleepTime)

            # check if Extract Filtering text appears in the page
            extractFilteringFound = re.search(r'Extract Filtering', driver.page_source)
            self.assertNotEqual(extractFilteringFound, None)

        except Exception as e:
            self.fail('Failed to login. Cause: %s' % e)

    '''
    Run test cases
    @para number: test case number
    '''
    def runTest(self, number):

        print("\nTest case "+number+"\n")

        driver = self.driver

        # log in
        self.test_log_in() 
        # got to dataset tab
        self.goToDatasetTab(driver)

        section = 'Test' + number + 'DatasetsParamsSection'
        subSection = 'datasets'

        # get parameter values from config file
        exportFormat = config.get(section, subSection + '.exportFormat') # export format
        principalInvestigator = config.get(section, subSection + '.principalInvestigator') # principal investigator
        project = config.get(section, subSection + '.project') # project
        experiment = config.get(section, subSection + '.experiment') # eperiment
        datasets = config.get(section, subSection + '.datasets').split("\n") # datasets name
        mapset = config.get(section, subSection + '.mapset') #mapset

        # dropdown fields
        opts = [ 
            principalInvestigator,
            project,
            experiment,
            mapset
        ]

        try:
            # select datasets parameters
            self.selectDatasetsParams(opts, exportFormat, driver)
            # select datasets
            self.selectDatasets(datasets, driver)
            # click submit button
            self.submit(driver)

        except Exception as e:
            self.fail('Failed to extract datasets. Cause: %s' % e)

        time.sleep(sleepTime)

    # Test case 1 Extractor UI Datasets testing
    def test_1_extractorui_datasets(self):
        self.runTest('1')

    # Test case 2 Extractor UI Datasets testing
    def test_2_extractorui_datasets(self):
        self.runTest('2')

    # Test case 3 Extractor UI Datasets testing
    def test_3_extractorui_datasets(self):
        self.runTest('3')

    # Test case 4 Extractor UI Datasets testing
    def test_4_extractorui_datasets(self):
       self.runTest('4')

    # Test case 5 Extractor UI Datasets testing
    def test_5_extractorui_datasets(self):
        self.runTest('5')

    # click "By Dataset" tab
    def goToDatasetTab(self, driver):
        # click By dataset tab
        datasetTab = driver.find_element_by_xpath(datasetTabXpath)
        datasetTab.click()

    '''
    Select values in dropdown list if value exists in config file
    Select export format
    @param exportFormat: export format
    @param opts: dropdown fields
    '''
    def selectDatasetsParams(self, opts, exportFormat, driver):
        # dropdown fields
        dropdownFields = [ 
            [principalInvestigatorXpath, opts[0], 'Principle Investigators'],
            [projectXpath, opts[1], 'Projects'],
            [experimentXpath, opts[2], 'Experiments'],
            [mapsetXpath, opts[3], 'Mapset']
        ]

        # loop through dropdown list fields, select value 
        for dropdownField in dropdownFields:                
            try:
                # if value is defined in the config file
                if(dropdownField[1] != None):
                    dropdownFieldObj = Select(driver.find_element_by_xpath(dropdownField[0]))
                    dropdownFieldObj.select_by_visible_text(dropdownField[1])
                    print("Selected %s: %s" % (dropdownField[2], dropdownField[1]))

                time.sleep(sleepTime)
            
            except(NoSuchElementException, TimeoutException) as e:
                # If value could not be found in the dropdown list
                self.fail("Test failed: %s %s could not be found in the list" % (dropdownField[1], dropdownField[2]))
            
        # find export format field and clicks a value, access shadow root element
        exportFormatField = driver.execute_script('return document.querySelector("export-format").shadowRoot.querySelectorAll("p-radiobutton[value=\''+exportFormat+'\']")[0]')
        exportFormatField.click()        
        print("Selected Export format:", exportFormat)
        time.sleep(sleepTime)

    '''
    Select datasets
    @param datasets: datasets to be selected
    '''
    def selectDatasets(self, datasets, driver):
        try:
            # loop through the datasets and check the checkbox
            for name in datasets:
                dataset = driver.find_element_by_id("DATASET_ROW_CHECKBOX_"+name.strip())
                dataset.click()
                print("Selected Dataset:", name)

                time.sleep(sleepTime)
        except(NoSuchElementException, TimeoutException) as e:
                # If dataset could not be found in the list
                self.fail("Test failed. Dataset could not be found. Error: %s " % e)

    # Click submit button and check if successfully extracted
    def submit(self, driver):
        # click submit button
        submitButton = driver.find_element_by_xpath(submitButtonXpath)
        submitButton.click()

        time.sleep(sleepTime)

        # check if success notification appeared
        successNotifFound = re.search(r'Extractor instruction file created on server: ', driver.page_source)
        self.assertNotEqual(successNotifFound, None)

    @classmethod
    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    if len(sys.argv) == 2: # if mode is set
        ExtractorUITest.mode = sys.argv.pop()
    else:
        ExtractorUITest.mode = 1 # default is normal mode
    
    # Generate test reports in xml file
    with open('test-reports/loading_test_results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))