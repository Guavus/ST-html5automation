from selenium.webdriver.support.wait import WebDriverWait
from time import time
from Utils.logger import *

class CustomWebDriverWait(WebDriverWait):
    def __init__(self,driver,timeout):
        super(CustomWebDriverWait,self).__init__(driver, timeout)

    def until(self, method, message=''):
        try:
            startTime = time()
            super(CustomWebDriverWait,self).until(method)
            timeTaken = time() - startTime
            logger.debug("Time Taken for %s element :: %s seconds", method.locator[1],timeTaken)
        except Exception as e:
            pass
            # print "Element not found", method.locator[1]
