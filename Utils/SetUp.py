from Utils.utility import *
from classes.DriverHelpers.DriverHelper import *
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import *
import os
import platform



class SetUp:
    def __init__(self,browser=Constants.BROWSER):

        if platform.system() == "Windows":
            delimiter = "\\"
        else:
            delimiter = "/"

        if Constants.SECURITY:
            if "chrome" == browser:
                os.system("mkdir "+Constants.chromdownloadpath)
                removeFileAtGivenPath(Constants.chromdownloadpath)

                chromeOptions = webdriver.ChromeOptions()
                # chromeOptions.add_argument("--kiosk")
                chromeOptions.add_argument("--start-maximized")
                exp_options = {}
                exp_options['profile.default_content_settings.popups'] = 0
                downloadFilepath = Constants.chromdownloadpath
                exp_options['download.default_directory'] = downloadFilepath
                chromeOptions.add_experimental_option("prefs", exp_options)

                # self.d = webdriver.Firefox()
                self.d = webdriver.Chrome(Constants.chromedriverpath, chrome_options=chromeOptions)
            elif "ff" == browser:
                os.system("mkdir "+Constants.firefoxdownloadpath)
                removeFileAtGivenPath(Constants.firefoxdownloadpath)
                fp = webdriver.FirefoxProfile()
                fp.set_preference("browser.download.folderList", 2)
                fp.set_preference("browser.download.manager.showWhenStarting", False)
                fp.set_preference("browser.download.dir",Constants.firefoxdownloadpath)

                fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-exceltext/csv,application/csv,application/octet-stream")

                fp.set_preference("browser.helperApps.alwaysAsk.force", False)
                #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
                fp.set_preference("browser.tabs.remote.autostart", False)
                fp.set_preference("browser.tabs.remote.autostart.1", False)
                fp.set_preference("browser.tabs.remote.autostart.2", False)
                fp.set_preference("security.insecure_password.ui.enabled", False);
                fp.set_preference("security.insecure_field_warning.contextual.enabled", False);


                self.d = webdriver.Firefox(executable_path=Constants.firefoxdriverpath,firefox_profile=fp)
            elif "safari" == browser:
                self.d = webdriver.Safari()



            # self.d = webdriver.Chrome(Constants.chromedriverpath)
        else:
            os.system("mkdir " + Constants.chromdownloadpath)
            removeFileAtGivenPath(Constants.chromdownloadpath)

            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--disable-web-security")
            chromeOptions.add_argument("--user-data-dir")
            chromeOptions.add_argument("--start-maximized")
            exp_options = {}
            exp_options['profile.default_content_settings.popups'] = 0
            downloadFilepath = Constants.chromdownloadpath
            exp_options['download.default_directory'] = downloadFilepath
            chromeOptions.add_experimental_option("prefs", exp_options)
            self.d = webdriver.Chrome(Constants.chromedriverpath,chrome_options=chromeOptions)


        # firefox_capabilities = DesiredCapabilities.FIREFOX
        # firefox_capabilities['marionette'] = True
        # firefox_capabilities['binary'] = '/Users/mayank.mahajan/node_modules/geckodriver/geckodriver'
        #
        #
        # executable_path ='/Users/mayank.mahajan/node_modules/geckodriver/geckodriver'
        # binary = FirefoxBinary('/Applications/Firefox.app')
        # self.d = webdriver.Firefox(capabilities=firefox_capabilities,firefox_binary=binary,executable_path=executable_path)


        # self.d = webdriver.Firefox()
        self.d.get(Constants.URL)
        self.d.set_window_size(1280,1024)
        # self.d.maximize_window()
        self.dH = DriverHelper(self.d)
        self.cM = ConfigManager()

