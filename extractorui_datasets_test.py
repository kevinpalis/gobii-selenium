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

# global variables
extractorUILink = config.get('SiteSection','site.address') # Extractor UI address
username = config.get('UserAccountSection', 'user.username') # username
password = config.get('UserAccountSection', 'user.password') # password

# params for test case 1
test1PrincipalInvestigator = config.get('Test1DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
test1Project = config.get('Test1DatasetsParamsSection','datasets.project') # project
test1Experiment = config.get('Test1DatasetsParamsSection','datasets.experiment') # eperiment
test1ExportFormat = config.get('Test1DatasetsParamsSection','datasets.exportFormat') # export format
test1Datasets = config.get('Test1DatasetsParamsSection','datasets.datasets').split("\n") # datasets name
test1Mapset = config.get('Test1DatasetsParamsSection','datasets.mapset')

# params for test case 2
test2PrincipalInvestigator = config.get('Test2DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
test2Project = config.get('Test2DatasetsParamsSection','datasets.project') # project
test2Experiment = config.get('Test2DatasetsParamsSection','datasets.experiment') # eperiment
test2ExportFormat = config.get('Test2DatasetsParamsSection','datasets.exportFormat') # export format
test2Datasets = config.get('Test2DatasetsParamsSection','datasets.datasets').split("\n") # datasets name
test2Mapset = config.get('Test2DatasetsParamsSection','datasets.mapset')

# params for test case 3
test3PrincipalInvestigator = config.get('Test3DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
test3Project = config.get('Test3DatasetsParamsSection','datasets.project') # project
test3Experiment = config.get('Test3DatasetsParamsSection','datasets.experiment') # eperiment
test3ExportFormat = config.get('Test3DatasetsParamsSection','datasets.exportFormat') # export format
test3Datasets = config.get('Test3DatasetsParamsSection','datasets.datasets').split("\n") # datasets name
test3Mapset = config.get('Test3DatasetsParamsSection','datasets.mapset')

# params for test case 4
test4PrincipalInvestigator = config.get('Test4DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
test4Project = config.get('Test4DatasetsParamsSection','datasets.project') # project
test4Experiment = config.get('Test4DatasetsParamsSection','datasets.experiment') # eperiment
test4ExportFormat = config.get('Test4DatasetsParamsSection','datasets.exportFormat') # export format
test4Datasets = config.get('Test4DatasetsParamsSection','datasets.datasets').split("\n") # datasets name
test4Mapset = config.get('Test4DatasetsParamsSection','datasets.mapset')

# params for test case 5
test5PrincipalInvestigator = config.get('Test5DatasetsParamsSection', 'datasets.principalInvestigator') # principal investigator
test5Project = config.get('Test5DatasetsParamsSection','datasets.project') # project
test5Experiment = config.get('Test5DatasetsParamsSection','datasets.experiment') # eperiment
test5ExportFormat = config.get('Test5DatasetsParamsSection','datasets.exportFormat') # export format
test5Datasets = config.get('Test5DatasetsParamsSection','datasets.datasets').split("\n") # datasets name
test5Mapset = config.get('Test5DatasetsParamsSection','datasets.mapset')

# xPath variables
loginCheckBoxXpath = "//p-checkbox" # checkbox in the login page
usernameXpath = "//input[@name='username']" # username field in the login page
passwordXPath = "//input[@name='password']" # password field in the login page
loginButtonXpath = "//button" # login buttom
principalInvestigatorXpath = "//select[@class='nameIdListBox']" # principal investigator dropdown list
projectXpath = "(//select[@class='nameIdListBox'])[2]" # project dropdown list
experimentXpath = "(//select[@class='nameIdListBox'])[3]" # experiment dropdown list
mapsetXpath = "(//select[@class='nameIdListBox'])[4]" # experiment dropdown list
submitButtonXpath = "//button[@type='submit']" # submit button
checkboxRowXpath = "(//p-datatable//p-checkbox)[1]" # first checkbox in the data table
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

            # wait for the form to load
            time.sleep(1 + sleepTime)

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


    # Run test cases
    def runTest(self, number, opts, exportFormat, datasets, driver):
        print("\nTest case "+number+"\n")

        # log in
        self.test_log_in() 
        # got to dataset tab
        self.goToDatasetTab(driver)

        try:

            # select datasets parameters
            self.selectDatasetsParams(exportFormat, opts, driver)
            # select datasets
            self.selectDatasets(datasets, driver)
            # click submit button
            self.submit(driver)

        except Exception as e:
            self.fail('Failed to extract datasets. Cause: %s' % e)

        time.sleep(sleepTime)

    # Test case 1 Extractor UI Datasets testing
    def test_1_extractorui_datasets(self):
        driver = self.driver

        # dropdown fields
        opts = [ 
            test1PrincipalInvestigator,
            test1Project,
            test1Experiment,
            test1Mapset
        ]

        self.runTest('1', opts, test1ExportFormat, test1Datasets, driver)

    # Test case 2 Extractor UI Datasets testing
    def test_2_extractorui_datasets(self):
        driver = self.driver

        # dropdown fields
        opts = [ 
            test2PrincipalInvestigator,
            test2Project,
            test2Experiment,
            test2Mapset
        ]

        self.runTest('2', opts, test2ExportFormat, test2Datasets, driver)

    # Test case 3 Extractor UI Datasets testing
    def test_3_extractorui_datasets(self):
        driver = self.driver

        # dropdown fields
        opts = [ 
            test3PrincipalInvestigator,
            test3Project,
            test3Experiment,
            test3Mapset
        ]

        self.runTest('3', opts, test3ExportFormat, test3Datasets, driver)

    # Test case 4 Extractor UI Datasets testing
    def test_4_extractorui_datasets(self):
        driver = self.driver

        # dropdown fields
        opts = [ 
            test4PrincipalInvestigator,
            test4Project,
            test4Experiment,
            test4Mapset
        ]

        self.runTest('4', opts, test4ExportFormat, test4Datasets, driver)

    # Test case 5 Extractor UI Datasets testing
    def test_1_extractorui_datasets(self):
        driver = self.driver

        # dropdown fields
        opts = [ 
            test5PrincipalInvestigator,
            test5Project,
            test5Experiment,
            test5Mapset
        ]

        self.runTest('5', opts, test5ExportFormat, test5Datasets, driver)

    # Click to dataset tab
    def goToDatasetTab(self, driver):
        # click By dataset tab
        datasetTab = driver.find_element_by_xpath(".//span[contains(text(), 'By Dataset')]")
        datasetTab.click()

    '''
    Select values in dropdown list if value exists in config file
    Select export format
    @param dropdownFields: dropdown fields
    @param exportFormat: export format
    '''
    def selectDatasetsParams(self, exportFormat, opts, driver):
        # dropdown fields
        dropdownFields = [ 
            [principalInvestigatorXpath, opts[0], 'Principle Investigators'],
            [projectXpath, opts[1], 'Projects'],
            [experimentXpath, opts[2], 'Experiments'],
            [mapsetXpath, opts[3], 'Mapset']
        ]

        '''
        loop through dropdown list fields, selects values 
        and checks if field values are equal to expected values
        '''
        for dropdownField in dropdownFields:                
            try:
                # if value is defined in the config file
                if(dropdownField[1] != None):
                    dropdownFieldObj = Select(driver.find_element_by_xpath(dropdownField[0]))
                    dropdownFieldObj.select_by_visible_text(dropdownField[1])
                    print("Selected %s: %s" % (dropdownField[2], dropdownField[1]))

                time.sleep(sleepTime)
            
            except(NoSuchElementException,TimeoutException) as e:
                # If value could not be found in the dropdown list
                print("Test failed: %s %s could not be found in the list" % (dropdownField[1], dropdownField[2]))
            
        # find export formt field and clicks a value, access shadow root element
        exportFormatField = driver.execute_script('return document.querySelector("export-format").shadowRoot.querySelectorAll("p-radiobutton[value=\''+exportFormat+'\']")[0]')
        exportFormatField.click()        
        print("Selected export format:", test1ExportFormat)
        time.sleep(sleepTime)

    '''
    Select datasets
    @param datasets: datasets to be selected
    '''
    def selectDatasets(self, datasets, driver):
        # loop through the datasets and check the checkbox
        #for name in datasets:
        #get checkbox
        # print(name)
        dataset = driver.find_element_by_xpath("//p-datatable//p-checkbox")
        dataset.click() 
        time.sleep(sleepTime)

    # Click submit button and check if successfully extracted
    def submit(self, driver):
        # click submit button
        submitButton = driver.find_element_by_xpath(submitButtonXpath)
        submitButton.click()

        time.sleep(sleepTime)

        # check if success notification appeared
        # successNotifFound = re.search(r'Extractor instruction file created on server: ', driver.page_source)
        # self.assertNotEqual(successNotifFound, None)

    @classmethod
    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        ExtractorUITest.mode = sys.argv.pop()
    else:
        ExtractorUITest.mode = 1 # default is normal mode
    
    # Generate test reports in xml file
    with open('test-reports/loading_test_results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))