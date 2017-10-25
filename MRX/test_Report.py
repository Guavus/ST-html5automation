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

    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    ############################ Verify reports can be downloaded using "Download" button present in table
    tableHandle['table']['download'][0].click()
    num_of_files_downoaded = len([name for name in os.listdir(Constants.firefoxdownloadpath) if not name.startswith('.') and os.path.isfile(os.path.join(Constants.firefoxdownloadpath, name))])
    checkEqualAssert(1, num_of_files_downoaded, message='Verify report gets successfully downloaded', testcase_id='MKR-3828')


    ############################ Verify table contains data and data can be sorted on each column
    ReportHelper.VerifyBasicTableFuncationality(setup,reportScreenInstance,MRXConstants.ReportScreenTableHeaderList)

    #############################  Verify data under table can be deleted with "Delete" button

    column1_ValuesFromTable = reportScreenInstance.table.getColumnValueFromTable(1, tableHandle)
    tableMap_beforeDelete = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup,colIndex=1)
    deleteFlag = reportScreenInstance.table.clickIconOnTableThroughTableHandle(tableHandle,value=str(column1_ValuesFromTable[0]),driver=setup.d,colIndexForKey=1)
    actaulResult_Flag = False
    if deleteFlag:
        confirmPopup = confirm_Popup(setup,segment_name=str(column1_ValuesFromTable[0]),screenName="report")
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        tableMap_afterDelete = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup, colIndex=1)

        actaulResult_Flag = len(tableMap_afterDelete) == len(tableMap_beforeDelete) and not (tableMap_afterDelete['rows'].has_key(str(column1_ValuesFromTable[0])))


    checkEqualAssert(True, actaulResult_Flag, message='Verify a row can be deleted successfully')

    #############################  Check if refresh icon is clickable
    #myscript = "execute_script('return arguments[0].click();',iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name('refresh-icon')[0])"
    #iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name("refresh-icon")[0]
    #setup.d.execute_script("document.getElementsByClassName('marx-report-grid-view')[0]")
    iconHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'icons')
    #click_status = setup.d.execute_script(myscript)
    click_status = setup.d.execute_script("return arguments[0].click();",iconHandle['icons']['refreshIcon'][0].find_elements_by_class_name("refresh-icon")[0])
    #checkEqualAssert(True,click_status , message='Verify that "Refresh" button just above the Report table is clickable')


    setup.d.close()



except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()



