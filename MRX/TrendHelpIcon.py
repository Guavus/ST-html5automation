from Utils.SetUp import *
from MRXUtils.MRXConstants import *
from MRXUtils import UDHelper
from classes.Components.WorkflowStartComponent import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Pages.ExplorePageClass import *

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    wfstart.launchScreen("Trend",getHandle(setup,MRXConstants.WFSTARTSCREEN))
    sleep(MRXConstants.SleepForTNMScreen)
    exploreScreenInstance = ExplorePageClass(setup.d)
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")

    availableDrillDownOption=exploreScreenInstance.cm.getAvailableOptionOnDrillDown(getHandle(setup,MRXConstants.TMSCREEN,"trend-header"),parent='trend-header')
    checkEqualAssert(MRXConstants.ExpectedDrillDownOptionOnTM,availableDrillDownOption,message="Validate the Drill Down button",testcase_id="MKR-3776")
    # exploreScreenInstance.cm.activate(getHandle(setup,MRXConstants.TMSCREEN,"trend-header"),parent='trend-header')
    # check_click=exploreScreenInstance.cm.goto("Create Segment",getHandle(setup, MRXConstants.TMSCREEN,"trend-header"),parent='trend-header')
    # addedSegmentDetail,detailFromPopup_Dict,textFromPopUp =UDHelper.createSmegmentFromUD(setup,TMScreenInstance,segmentDetail)

    clickFlag=exploreScreenInstance.exploreList.clickOnIcon(exploreHandle)
    if clickFlag:
        clickHelpFlag=exploreScreenInstance.exploreList.launchModule(getHandle(setup, "explore_Screen"),'Help')
        if clickHelpFlag:
            setup.d.switch_to.window(setup.d.window_handles[1])
            checkEqualAssert(True,'help' in str(setup.d.current_url).lower(),message="Verify the functionality of the help button",testcase_id="MKR-3775")
            setup.d.close()
            setup.d.switch_to.window(setup.d.window_handles[0])
        else:
            checkEqualAssert(True, clickHelpFlag,message="Verify the functionality of the help button",testcase_id="MKR-3775")
    else:
        checkEqualAssert(True,clickFlag,message="Verify the functionality of the help button",testcase_id="MKR-3775")


    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved<br>", r)
    setup.d.close()