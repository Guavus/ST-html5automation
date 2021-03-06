import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.GenerateReportsPopClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)


# Checking drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)

nescreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

# Export to csv
exportTo(setup,setup.dH,'EXPORTTOSNAPSHOT')
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup")
result = grPopInstance.reportspopup.clickButton("Download",grPopHandle)
# Result logging
checkEqualAssert(result,True,"","","EXPORT TO SNAPSHOT network elements")

#Closing the application
setup.d.close()