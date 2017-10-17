from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.ReportScreenClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import ReportHelper

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)

    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    screen_status = exploreScreenInstance.exploreList.launchModule(exploreHandle, "REPORT")
    checkEqualAssert(True, screen_status, message='Verify Reports tab gets opened successfully', testcase_id='MKR-3517')

    reportScreenInstance = ReportScreenClass(setup.d)
    '''
    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    tableHandle['table']['download'][0].click()
    '''

    ReportHelper.VerifyBasicTableFuncationality(setup,reportScreenInstance,MRXConstants.ReportScreenTableHeaderList)

    #############################  Check if refresh icon is clickable
    #myscript = "execute_script('return arguments[0].click();',iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name('refresh-icon')[0])"
    #iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name("refresh-icon")[0]
    #setup.d.execute_script("document.getElementsByClassName('marx-report-grid-view')[0]")
    iconHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'icons')
    #click_status = setup.d.execute_script(myscript)
    click_status = setup.d.execute_script("return arguments[0].click();",iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name("refresh-icon")[0])
    #checkEqualAssert(True,click_status , message='Verify that "Refresh" button just above the Report table is clickable',testcase_id='MKR-1675')


    setup.d.close()



except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()



