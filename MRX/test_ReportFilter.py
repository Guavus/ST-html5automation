import unittest
from MRXUtils import ReportHelper
from Utils.logger import *
from selenium import webdriver
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.ReportScreenClass import ReportScreenClass
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *

try:

    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "REPORT")

    reportScreenInstance = ReportScreenClass(setup.d)

    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    data2 = reportScreenInstance.table.getTableData1(tableHandle,length=20)


### Verify Filter button just above the Report table is clickable

    click_status=ReportHelper.clickOnfilterIcon(setup,MRXConstants.REPORTSCREEN,'nofilterIcon')
    checkEqualAssert(True,click_status,message='Verify that "Filter" button just above the Report table is clickable')


###  Verify Filter Header Text on Filter Popup

    filterScreenHandle=getHandle(setup,MRXConstants.FILTERSCREEN)
    checkEqualAssert("Report Filters",str(filterScreenHandle['allspans']['span'][0].text),message="Verify Filter Header Text on Filter Popup")
    allSpanList = []
    actualFilters_onFilterPopup = []
    for ele in filterScreenHandle['allspans']['span']:
        allSpanList.append(str(ele.text))
        actualFilters_onFilterPopup = [item for item in allSpanList if item != "" and item != "Report Filters"]
    Keys = setup.cM.getAllNodeElements("report_Filters", "filter")
    expectedFilters_onFilterPopup = Keys + ['Select']
    checkEqualAssert(True, set(expectedFilters_onFilterPopup) == set(actualFilters_onFilterPopup),message='Verify available Filter Expected= ' + str(expectedFilters_onFilterPopup) + ' Actual Available Set= ' + str(actualFilters_onFilterPopup))


####  Verify available button on filter screen ####################################################################################################################

    availableButtonList=[]
    for button in filterScreenHandle['allbuttons']['button']:
        availableButtonList.append(str(button.text))
    availableButtonList.append(str(len(filterScreenHandle['icons']['closePopupIcon'])))
    actualButtonList=['Apply Filters','Cancel','Clear All','1']
    checkEqualAssert(actualButtonList,availableButtonList,'','','Verify available button on filter screen')
    ReportHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN, 'closePopupIcon', parent='icons')

    #### Verify text of all filters present in filter popup matches with those present in the table

    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, "table")
    tableMap = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    tableMap_finalHeaderList = [item for item in tableMap['header'] if item != "Download" and item != "Delete" and item != "Id"]
    actualFilters_onFilterPopup.remove("Select")
    checkEqualAssert(True, actualFilters_onFilterPopup == tableMap_finalHeaderList, '', '', 'Verify text of all filters present in filter popup matches with those present in the table' + "----Text in filter popup: "+str(actualFilters_onFilterPopup) + "----Text in table header: " +str(tableMap_finalHeaderList), testcase_id='MKR-3635')

    ### Verify Filters Selections from Tooltip on the Report Screen #####################################################################################################################

    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
    expected = ReportHelper.setReportFilter(setup,reportScreenInstance,k=0)
    reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)
    popUpTooltipData = ReportHelper.getGlobalFiltersToolTipData(MRXConstants.REPORTSCREEN, reportScreenInstance, setup,flag=False)
    checkEqualDict(expected,popUpTooltipData,message="Verify Filters Selections from Tooltip on Report Screen",testcase_id='MKR-3673')


### Verify Filters Selections from Report Screen  #####################################################################################################################

    filterFromScreen=ReportHelper.getGlobalFiltersFromScreen(MRXConstants.REPORTSCREEN, reportScreenInstance, setup,flag=False)
    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN,'filterIcon')
    expectedFromFilterPopUp = ReportHelper.getReportFilter(setup, reportScreenInstance)
    checkEqualDict(filterFromScreen, expectedFromFilterPopUp,message="Verify Filters Selections from Report Screen")


### Verify Clear all Functionality for Filter on Filter-Popup Screen
    reportScreenInstance.cm.clickButton("Clear All", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    expectedFromFilterPopUpAfterClear = ReportHelper.getReportFilter(setup, reportScreenInstance)
    BlankDict=ReportHelper.insertKeys({},Keys)
    checkEqualDict(BlankDict,expectedFromFilterPopUpAfterClear,message='Verify Clear all Functionality for Filter on Filter-Popup Screen')

    reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    data3 = reportScreenInstance.table.getTableData1(tableHandle,length=20)
    checkEqualAssert(data2['rows'], data3['rows'],message='Checked Clear all Functionality for Filter on Report Screen by verifying number of records visible under table')


###  Verify X(cross)button on filter popup clears all the filters applied  #####################################################################################################################

    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
    expected = ReportHelper.setReportFilter(setup, reportScreenInstance, k=0)
    try:
        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN,'closePopupIcon',parent='icons')
    except:
        try:
            click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN, 'closePopupIcon',parent='icons')
        except:
            pass

    if click_status:
        checkEqualAssert(0,len(getHandle(setup,MRXConstants.FILTERSCREEN,'icons')['icons']['closePopupIcon']),message='On pressing the "X", the filter window dissappears')
        filterFromScreenAfterClear=ReportHelper.getGlobalFiltersFromScreen(MRXConstants.REPORTSCREEN, reportScreenInstance, setup,flag=False)
        checkEqualAssert(MRXConstants.NO_FILTER, str(filterFromScreenAfterClear),message='After press cross (X), no filters should be seen on Report Screen')

####  Verify on pressing "Cancel" button the filter window disappears

    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
    reportScreenInstance.cm.hoverAndClickButton(setup=setup,value="Cancel", h=getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))

    checkEqualAssert(0, len(getHandle(setup, MRXConstants.FILTERSCREEN, 'allsliders')['allsliders']['slider']), message='On pressing the "Cancel" button the filter window dissappears')


####  Verify "Help" icon on Filter Popup is clickable

    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
    try:
        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN, 'helpIcon', parent='icons')
    except:
        try:
            click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN, 'helpIcon', parent='icons')
        except:
            pass

    checkEqualAssert(True, click_status, message='Verify Help icon on Filter Popup is clickable')
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()
