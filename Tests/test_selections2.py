import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *




# Getting Setup Details
setup = SetUp()


# Launching Application
login(setup, "admin", "Admin@123")


# launchPage(setup,"site_Screen")
# siteScreenInstance = SitePageClass(setup.d)
# siteScreenHandle = getHandle(setup,"site_Screen")
#
# data = siteScreenInstance.btv.getData(siteScreenHandle)

# Launch Screen
launchPage(setup,"nf_Screen")

# GetScreenInstance and control over its Components
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,"nf_Screen")

# setSearch = nfScreenInstance.searchComp.setSearchText(nfScreenHandle,"mayank")
# time.sleep(2)
# nfScreenInstance.searchComp.setSearchText(nfScreenHandle,Keys.BACK_SPACE)
# time.sleep(2)
# # Keys.BACK_SPACE
#
# text = nfScreenInstance.searchComp.getSearchText(nfScreenHandle)
#
# if(setSearch==True):
#     nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
# else:
#     # checkEqualAssert() LOG result Exception
#     pass
#
# #clears the search
# nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)




selections = nfScreenInstance.summarybar.getSelection(nfScreenHandle)


# Log Result
# checkEqualAssert(piedata['legendText'],piedata['tooltipdata'],"NA","NA","Pie Tooltip Validations at NFScreen")

time.sleep(10)

# Closing the Testcase
setup.d.close()