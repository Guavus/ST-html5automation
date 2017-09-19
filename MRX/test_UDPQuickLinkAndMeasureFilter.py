from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    udScreenInstance.wfstart.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
    time.sleep(5)

    measures = ConfigManager().getNodeElements("ud_measures", "measure")
    mes = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])

    qs = ConfigManager().getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = ConfigManager().getAllNodeElements("wizardquicklinks1", "wizardquicklink")
    flag=True

    for m in range(len(mes)):
        chartAndTableFlag=True
        selectedMeasure = udScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDSCREEN, "allselects"), str(mes[m]), index=0, parent="allselects")
        for e in quicklink:
            udScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'], getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
            isError(setup)
            selectedQuicklink = udScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))
            t1 = udScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDSCREEN, "ktrs"))

            if flag:
                t = TimeRangeComponentClass().get_Label(e)
                checkEqualAssert(t[1], t1, selectedQuicklink, selectedMeasure, message="Verify quicklink label")

            timeRangeFromPopup = str(t1).strip()
            measureFromPopup = str(selectedMeasure).strip()

            h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
            timeRangeFromScreen = str(h['time_measure']['span'][0].text).strip()
            measureFromScreen = udScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDSCREEN, "allselects"))

            checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,selectedQuicklink,selectedMeasure,message='Verify Selected Quicklink applied successfully')
            checkEqualAssert(measureFromPopup,measureFromScreen,selectedQuicklink,selectedMeasure,message='Verify Selected Measure applied successfully')
            testidForChart,testidForGrid = UDHelper.getTestCaseID(selectedMeasure)

            Data_label = str(getHandle(setup, MRXConstants.UDSCREEN, 'body')['body']['data_label'][0].text).strip()
            if Data_label == Constants.NODATA:
                checkEqualAssert(False, True, selectedQuicklink, selectedMeasure,message="Verify Chart and Grid gets plotted for selected measure and quicklink",testcase_id=testidForChart + "," + testidForGrid)
            else:
                if len(getHandle(setup,MRXConstants.UDSCREEN,'body')['body']['lineChartComponent'])>0:
                    if chartAndTableFlag:
                        xAxisPointList=UDHelper.getAxisPoint(getHandle(setup,MRXConstants.UDSCREEN,'body'))
                        hoverData = UDHelper.hoverOverTicksGetMainChartText(setup,getHandle(setup, MRXConstants.UDSCREEN,'body'))
                        if 'header' in hoverData.keys():
                            checkEqualAssert(selectedMeasure,hoverData['header'][1].lstrip('Cumulated').strip(),selectedQuicklink,selectedMeasure,message='Verify that no unit is assign to any variable (Chart View)',testcase_id='MKR-2765')
                        exactData = UDHelper.exactDataFromChart(hoverData,selectedMeasure)
                        UDHelper.validateRangeAndSortingInChart(xAxisPointList,exactData,selectedQuicklink, selectedMeasure)

                    chartPlotted=True
                else:
                    chartPlotted=False

                checkEqualAssert(True,chartPlotted,selectedQuicklink,selectedMeasure,message="Verify that on selecting " +str(selectedMeasure)+" metric for "+ selectedQuicklink+" time range the user distribution chart gets plotted for this metric",testcase_id=testidForChart)
                udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
                time.sleep(5)
                expectedHeader=['Range','Users','% of '+selectedMeasure,selectedMeasure,'Average '+selectedMeasure]
                tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
                data = udScreenInstance.table.getTableDataWithScroll(tableHandle, driver=setup)
                checkEqualAssert(expectedHeader,data['header'],selectedQuicklink,selectedMeasure,message="Verify that on selecting " +str(selectedMeasure)+" metric for "+ selectedQuicklink+" time range the user distribution Grid gets plotted And also Verify that no unit is assign to any variable (Table-View)",testcase_id=testidForGrid+' ,MKR-2765')

                checkEqualAssert(20, len(data['rows']), selectedQuicklink, selectedMeasure,message='Verify Number of rows in Table')
                if chartAndTableFlag:
                    UDHelper.validateRangeAndSortingInTable(udScreenInstance,data,selectedQuicklink,selectedMeasure)
                udScreenInstance.switcher.measureChangeSwitcher_UD(0,getHandle(setup, MRXConstants.UDSCREEN, "switcher"))

            chartAndTableFlag=False
        flag=False
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
