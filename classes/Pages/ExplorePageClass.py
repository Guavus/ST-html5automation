from BasePageClass import BasePageClass
from classes.Components.BaseComponentClass import *
from classes.Components.ExploreListComponentClass import *

class ExplorePageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.exploreList = ExploreListComponentClass()

        # Common Components
        BasePageClass.__init__(self, driver)

    def launchPage(self, elHandle):
        self.exploreList.click(elHandle)

    
