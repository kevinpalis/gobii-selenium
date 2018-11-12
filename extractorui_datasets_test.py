#!/usr/bin/env python
"""
GOBii Extracor UI Datasets testing

Steps:
1. Log in to ExtractorUI website with a given username and password defined in properties file
2. Loop through dropdown fields (i.e. Principal investigator, Projects and Experiment)
3. Selects values from the dropdown lists based from the defined values in properties file
4. Checks if items in the dropdown list are equal to the expected values defined in the properties file
5. Selects Export file format
6. Selects first row in the table to be extracted
7. Clicks submit button
8. Checks if extraction was successful
9. Exit

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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import ConfigParser
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import re

# get values from config properties file
config = ConfigParser.RawConfigParser()
config.read('ConfigFile.properties')

# global variables
extractorUILink = config.get('SiteSection','site.address') # Extractor UI address
username = config.get('UserAccountSection', 'user.username') # username
password = config.get('UserAccountSection', 'user.password') # password
principalInvestigator = config.get('DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
project = config.get('DatasetsParamsSection','datasets.project') # project
experiment = config.get('DatasetsParamsSection','datasets.experiment') # eperiment
exportFormat = config.get('DatasetsParamsSection','datasets.exportFormat') # export format

# expected dropdown list values
projectValues = config.get('DatasetsParamsSection','datasets.projectValues').split("\n") # project values
experimentValues = config.get('DatasetsParamsSection','datasets.experimentValues').split("\n") # experiment values

# xPath variables
loginCheckBoxXpath = "//p-checkbox" # checkbox in the login page
usernameXpath = "//input[@name='username']" # username field in the login page
passwordXPath = "//input[@name='password']" # password field in the login page
loginButtonXpath = "//button" # login buttom
principalInvestigatorXpath = "//select[@class='nameIdListBox']" # principal investigator dropdown list
projectXpath = "(//select[@class='nameIdListBox'])[2]" # project dropdown list
experimentXpath = "(//select[@class='nameIdListBox'])[3]" # experiment dropdown list
submitButtonXpath = "//button[@type='submit']" # submit button
checkboxRowXpath = "(//p-datatable//p-checkbox)[1]" # first checkbox in the data table

class ExtractorUITest(unittest.TestCase):

    # driver set up
    @classmethod
    def setUp(self):

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options)    

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

            # wait for the form to load
            time.sleep(4)

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
            time.sleep(2)

            # check if Extract Filtering text appears in the page
            extractFilteringFound = re.search(r'Extract Filtering', driver.page_source)
            self.assertNotEqual(extractFilteringFound, None)

        except Exception as e:
            self.fail('Failed to login. Cause: %s' % e)


    # Extractor UI Datasets testing
    def test_extractorui_datasets(self):
        
        driver = self.driver

        #log in
        self.test_log_in() 

        try:
            # dropdown fields
            dropdownFields = [ 
                [principalInvestigatorXpath, principalInvestigator, 'Principle Investigators', []],
                [projectXpath, project, 'Projects', projectValues],
                [experimentXpath, experiment, 'Experiments', experimentValues]
            ]

            '''
            loop through dropdown list fields, selects values 
            and checks if field values are equal to expected values
            '''
            for dropdownField in dropdownFields:                
                try:

                    dropdownFieldObj = Select(driver.find_element_by_xpath(dropdownField[0]))
                    dropdownFieldObj.select_by_visible_text(dropdownField[1])
                    print("Selected %s: %s" % (dropdownField[2], dropdownField[1]))

                    if(dropdownField[1] != principalInvestigator):
                        # include 'All + field' in the options
                        dropdownValuesUpdated = ['All ' + dropdownField[2]] + dropdownField[3]
                        # check if dropdown values equal 
                        self.checkIfDropdownValsEqual(dropdownFieldObj.options, dropdownValuesUpdated, dropdownField[2])

                    time.sleep(1)
                
                except(NoSuchElementException,TimeoutException) as e:
                    # If value could not be found in the dropdown list
                    print("Test failed: %s %s could not be found in the list" % (dropdownField[1], dropdownField[2]))
                
            # find export formt field and clicks a value, access shadow root element
            exportFormatField = driver.execute_script('return document.querySelector("export-format").shadowRoot.querySelectorAll("p-radiobutton[value=\''+exportFormat+'\']")[0]')
            exportFormatField.click()        
            print("Selected export format:", exportFormat)
            time.sleep(1)

            # checks first row in table
            dataTableVal = driver.find_element_by_xpath(checkboxRowXpath)
            dataTableVal.click()

            # click submit button
            submitButton = driver.find_element_by_xpath(submitButtonXpath)
            submitButton.click()

            time.sleep(2)

            # check if success notification appeared
            successNotifFound = re.search(r'Extractor instruction file created on server: ', driver.page_source)
            self.assertNotEqual(successNotifFound, None)

        except Exception as e:
            self.fail('Failed to extract datasets. Cause: %s' % e)

        time.sleep(2)

    '''
    Checks if dropdown values of an attribute are 
    equal to expected values defined in properties file
    @param dropdownOptions: options of the attribute (i.e. List options of Project dropdown field)
    @param expectedVals: expected values of the dropdown list
    @param attr: field that wants to be checked (i.e. Project)
    ''' 
    def checkIfDropdownValsEqual(self, dropdownOptions, expectedVals, attr):
        selectValsArr = []

        # loop through the dropdown options, strip the values and stores it in an array
        for opt in dropdownOptions:
            selectValsArr.append(opt.text.strip())

        # compares if project list is equal to that of in the config file
        isValsEqual = (selectValsArr==expectedVals) 

        if(isValsEqual):
            print("%s values are equal..." % attr)
        else:
            print("Failed. %s values are NOT equal..." % attr)
        
    @classmethod
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    # Generate test reports in xml file
    with open('test-reports/loading_test_results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))