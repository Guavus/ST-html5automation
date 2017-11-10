from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import SegmentHelper
from MRXUtils import TMHelper
from MRXUtils.TMHelper import *
from Utils.AvailableMethod import *
import json

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    tm_Click_Flag = wfstart.launchScreen("Trend", getHandle(setup, MRXConstants.WFSTARTSCREEN))
    sleep(MRXConstants.SleepForTNMScreen)
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)

    actualAvailableQuickLinkList = UDHelper.availableQuickLink(setup, MRXConstants.TMSCREEN)
    checkEqualAssert(MRXConstants.ExpectedQuickLinkList, actualAvailableQuickLinkList,message='Verify available quicklink for Trends')

    # TMHelper.setQuickLink_Measure_BreakDown(setup,TMScreenInstance, str('testCalender')) # Check Calender Scenario (Start Time > End Time)

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    udpHandle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    for dim in udpHandle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that on clicking Filter icon Filter window appears with all the possible fields on which filter can be applied")

    ################################# Validating Cancel Button Functionality ###########################################

    expected = {}
    expected = UDHelper.setUDPFilters(TMScreenInstance, setup, str(0), screen=MRXConstants.TMSCREEN)
    isError(setup)
    TMScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MRXConstants.ALLBUTTONS))
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.TMSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing Cancel button selected filters not get applied",testcase_id='')

    ################################# Validating Cross (X) Button Functionality ########################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(TMScreenInstance, setup, str(0),screen=MRXConstants.TMSCREEN)
    isError(setup)
    TMScreenInstance.clickIcon(getHandle(setup, MRXConstants.UDPPOPUP, 'icons'), setup.d, child='closePopupIcon')
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.TMSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing (X) button selected filters not get applied",testcase_id='')

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()



